.PHONY: help install setup install-precommit lint activate shell run-a2a run-a2a-remote run-a2a-ephemeral run-jobs-service run-team-api test-team-api serve-agents list-agents run-agent add-dep infra-init infra-apply infra-destroy setup-toolbox run-toolbox setup-terraform check-gcloud setup-sql-proxy deploy-toolbox deploy-agent infra-stop infra-start

UV := $(shell command -v uv 2> /dev/null)

help:
	@echo "🏢 Corporate AI Hub - Available Commands:"
	@echo ""
	@echo "🔧 Setup & Environment:"
	@echo "  make setup             - Install all binaries (uv, terraform, toolbox) and sync Python"
	@echo "  make lint              - Run ruff, mypy, and pyright checks"
	@echo ""
	@echo "🏗️ Infrastructure (Terraform):"
	@echo "  make infra-init        - Initialize Terraform"
	@echo "  make infra-apply       - Deploy GCP resources (Cloud SQL, Spanner)"
	@echo "  make infra-destroy     - Teardown all GCP resources"
	@echo "  make infra-stop        - Pause Cloud SQL and Scale Down Spanner (Cost Saving)"
	@echo "  make infra-start       - Resume Cloud SQL and Scale Up Spanner"
	@echo "  make seed-db           - Seed Cloud SQL with jobs data"
	@echo "  make seed-spanner      - Seed Spanner with finance graph data"
	@echo ""
	@echo "🚀 Execution (Local Monolith):"
	@echo "  make run-toolbox       - Start MCP Toolbox (Middleware for SQL)"
	@echo "  make run-a2a           - Run Corporate Hub (Persistent Memory)"
	@echo "  make run-a2a-ephemeral - Run Corporate Hub (Short-term memory only)"
	@echo ""
	@echo "🌐 Execution (Remote A2A Services):"
	@echo "  make run-jobs-service  - Start Jobs Domain as a standalone service (Port 8001)"
	@echo "  make run-a2a-remote    - Run Orchestrator in Remote Discovery mode"
	@echo ""
	@echo "🖥️ UI & API:"
	@echo "  make serve-agents      - Start Web UI at http://localhost:8000"
	@echo "  make run-team-api      - Start Orchestrator as a FastAPI REST server"
	@echo ""
	@echo "☁️ Deployment (Cloud Run):"
	@echo "  make deploy-toolbox    - Deploy MCP Toolbox to Cloud Run"
	@echo "  make deploy-agent      - Deploy Orchestrator to Cloud Run"

install-uv:
ifndef UV
	@echo "Installing uv..."
	curl -LsSf https://astral.sh/uv/install.sh | ph
else
	@echo "uv is already installed."
endif

setup: install-uv setup-toolbox setup-terraform setup-sql-proxy
	@echo "Setting up Python environment..."
	cd python && uv sync

# MCP Toolbox binary setup
setup-toolbox:
	@if [ ! -f "./toolbox" ]; then \
		echo "Downloading MCP Toolbox binary..."; \
		curl -o toolbox https://storage.googleapis.com/genai-toolbox/v0.27.0/linux/amd64/toolbox; \
		chmod +x toolbox; \
	else \
		echo "MCP Toolbox binary already exists."; \
	fi

# Terraform setup
TF_VERSION := 1.10.0
setup-terraform:
	@if [ ! -f "./terraform" ]; then \
		echo "Downloading Terraform v$(TF_VERSION)..."; \
		curl -o terraform.zip https://releases.hashicorp.com/terraform/$(TF_VERSION)/terraform_$(TF_VERSION)_linux_amd64.zip; \
		unzip -o terraform.zip; \
		rm terraform.zip; \
		chmod +x terraform; \
	else \
		echo "Terraform binary already exists."; \
	fi

# Cloud SQL Proxy setup
setup-sql-proxy:
	@if ! command -v cloud-sql-proxy >/dev/null 2>&1 && [ ! -f "./cloud-sql-proxy" ]; then \
		echo "Downloading Cloud SQL Auth Proxy..."; \
		curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.14.2/cloud-sql-proxy.linux.amd64; \
		chmod +x cloud-sql-proxy; \
	else \
		echo "Cloud SQL Auth Proxy already exists."; \
	fi

# Check for gcloud
check-gcloud:
	@if command -v gcloud >/dev/null 2>&1; then \
		echo "gcloud is installed: $$(gcloud --version | head -n 1)"; \
	else \
		echo "ERROR: gcloud CLI is not installed. Please install it from: https://cloud.google.com/sdk/docs/install"; \
		exit 1; \
	fi

# Infrastructure
infra-init: setup-terraform
	@echo "Initializing Terraform..."
	./terraform -chdir=infra init

infra-apply: setup-terraform
	@echo "Applying Terraform configuration..."
	./terraform -chdir=infra apply

infra-stop: check-gcloud
	@echo "Pausing Cloud SQL instance..."
	@set -a && . ./.env && set +a; \
	gcloud sql instances patch jobs-db-instance --activation-policy=NEVER --project=$$GOOGLE_CLOUD_PROJECT --quiet
	@echo "Scaling Down Spanner instance to 100 Processing Units (Min Cost)..."
	@set -a && . ./.env && set +a; \
	gcloud spanner instances update finance-instance --processing-units=100 --project=$$GOOGLE_CLOUD_PROJECT --quiet

infra-start: check-gcloud
	@echo "Resuming Cloud SQL instance..."
	@set -a && . ./.env && set +a; \
	gcloud sql instances patch jobs-db-instance --activation-policy=ALWAYS --project=$$GOOGLE_CLOUD_PROJECT --quiet
	@echo "Scaling Up Spanner instance to 1 Node..."
	@set -a && . ./.env && set +a; \
	gcloud spanner instances update finance-instance --nodes=1 --project=$$GOOGLE_CLOUD_PROJECT --quiet

infra-destroy: check-gcloud setup-terraform
	@echo "Destroying all infrastructure (Cloud SQL, Spanner, etc.)..."
	./terraform -chdir=infra destroy -auto-approve
	@echo "Deleting Cloud Run services..."
	@set -a && . ./.env && set +a; \
	gcloud run services delete mcp-toolbox-service --region=$$REGION --project=$$GOOGLE_CLOUD_PROJECT --quiet 2>/dev/null || true; \
	gcloud run services delete adk-agents-service --region=$$REGION --project=$$GOOGLE_CLOUD_PROJECT --quiet 2>/dev/null || true; \
	echo "Cleaning up extra Cloud Run artifacts..."
	@set -a && . ./.env && set +a; \
	gcloud artifacts repositories delete cloud-run-source-deploy --location=$$REGION --quiet 2>/dev/null || true

# Deployment to Cloud Run (Source-based build)
deploy-toolbox: check-gcloud
	@echo "Deploying MCP Toolbox to Cloud Run..."
	@set -a && . ./.env && set +a; \
	cp toolbox python/mcp_servers/jobs_db/tools.yaml deploy/toolbox/; \
	gcloud run deploy mcp-toolbox-service \
		--source deploy/toolbox/ \
		--region $$REGION \
		--project $$GOOGLE_CLOUD_PROJECT \
		--set-env-vars DB_PASSWORD=$$DB_PASSWORD,GOOGLE_CLOUD_PROJECT=$$GOOGLE_CLOUD_PROJECT,REGION=$$REGION \
		--allow-unauthenticated

deploy-agent: check-gcloud
	@echo "Deploying ADK Agent Orchestrator to Cloud Run..."
	@set -a && . ./.env && set +a; \
	cp python/pyproject.toml python/uv.lock deploy/agent/; \
	cp -r python/agents deploy/agent/; \
	TOOLBOX_URL=$$(gcloud run services describe mcp-toolbox-service --region $$REGION --format 'value(status.url)'); \
	gcloud run deploy adk-agents-service \
		--source deploy/agent/ \
		--region $$REGION \
		--project $$GOOGLE_CLOUD_PROJECT \
		--set-env-vars TOOLBOX_URL=$$TOOLBOX_URL,GOOGLE_CLOUD_PROJECT=$$GOOGLE_CLOUD_PROJECT,REGION=$$REGION,ADK_AGENT=agents/orchestrator \
		--allow-unauthenticated

# Run MCP Toolbox
run-toolbox: setup-toolbox
	@echo "Running MCP Toolbox..."
	@set -a && . ./.env && set +a; \
	./toolbox --tools-file python/mcp_servers/jobs_db/tools.yaml

# Seed Database
seed-db: check-gcloud setup-sql-proxy
	@echo "Seeding the database..."
	@# Source the .env file to get DB_PASSWORD
	@set -a && . ./.env && set +a; \
	PGPASSWORD="$$DB_PASSWORD" PATH="$$PATH:$(PWD)" gcloud sql connect jobs-db-instance --user=jobs_user --project=$$GOOGLE_CLOUD_PROJECT --quiet < python/mcp_servers/jobs_db/cloud_sql_seed.sql

sync-env:
	@echo "Syncing Terraform outputs to .env..."
	@if [ ! -f ".env" ]; then cp .env.example .env; fi
	@PASS=$$(./terraform -chdir=infra output -raw db_password); \
	if [ -n "$$PASS" ]; then \
		sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=\"$$PASS\"/" .env; \
		echo "DB_PASSWORD synchronized."; \
	else \
		echo "Error: Could not retrieve password from Terraform. run make infra-apply first."; \
	fi

# Seed Spanner
seed-spanner: check-gcloud
	@echo "Seeding Spanner database..."
	@set -a && . ./.env && set +a; \
	gcloud spanner databases execute-sql finance-db --instance=finance-instance --project=$$GOOGLE_CLOUD_PROJECT --sql="$$(cat sql/spanner_seed.sql)"

install-precommit: setup
	@echo "Installing pre-commit hooks..."
	cd python && uv run pre-commit install --config ../.pre-commit-config.yaml

activate:
	@echo "To activate the virtual environment, run:"
	@echo "source python/.venv/bin/activate"

shell:
	@echo "Dropping into a shell with the virtual environment activated..."
	cd python && uv run bash

list-agents:
	@echo "Available Python agents:"
	@ls -d python/agents/*/ | xargs -n 1 basename

run-agent:
	@if [ -z "$(NAME)" ]; then \
		echo "Usage: make run-agent NAME=agent_directory_name"; \
		make list-agents; \
	else \
		echo "Running agent $(NAME)..."; \
		cd python && PYTHONPATH=agents uv run --env-file ../.env adk run agents/$(NAME); \
	fi

add-dep:
	@if [ -z "$(PKG)" ]; then \
		echo "Usage: make add-dep PKG=package_name"; \
		else \
		echo "Installing $(PKG) with uv..."; \
		cd python && uv add $(PKG); \
	fi

run-currency-mcp:
	@echo "Running Currency MCP Server..."
	cd python && uv run python mcp_servers/currency/server.py

run-a2a:
	@echo "Running Corporate Hub in LOCAL Monolith Mode (Persistent Memory)..."
	@$(MAKE) run-agent NAME=orchestrator

run-a2a-ephemeral:
	@echo "Running Corporate Hub in EPHEMERAL Mode (Short-term memory only)..."
	cd python && PERSISTENT_MEMORY=false uv run --env-file ../.env adk run agents/orchestrator

# REMOTE A2A Path
run-jobs-service:
	@echo "Starting standalone Jobs A2A Service on port 8001..."
	cd python && uv run python agents/jobs/main.py

run-a2a-remote:
	@echo "Running Corporate Hub in REMOTE A2A Mode (Discovery)..."
	cd python && USE_REMOTE_A2A=true JOBS_SERVICE_URL=http://localhost:8001 uv run --env-file ../.env adk run agents/orchestrator

run-team-api:
	@echo "Starting the Agent Orchestrator FastAPI server..."
	cd python && uv run uvicorn agents.orchestrator.main:app --host 0.0.0.0 --port 8000 --reload

test-team-api:
	@echo "Testing the Agent Orchestrator API..."
	curl -X POST "http://localhost:8000/chat" \
		 -H "Content-Type: application/json" \
		 -d '{"user_id": "test_user", "session_id": "test_session", "message": "Hi, I am Karol! What is the weather in Tokyo?", "temp_unit": "Celsius"}'
	@echo "\n"

serve-agents:
	@echo "Serving the agents web interface on port 8000..."
	cd python && uv run --env-file ../.env adk web agents --port 8000

lint:
	cd python && uv run ruff check . --fix
	cd python && uv run ruff format .
	cd python && uv run mypy .
	cd python && uv run pyright .
