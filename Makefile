.PHONY: install setup install-precommit lint activate shell run-single run-multi run-multimodal run-rag run-team-api test-team-api serve-agents list-agents run-agent add-dep infra-init infra-apply setup-toolbox run-toolbox setup-terraform check-gcloud

UV := $(shell command -v uv 2> /dev/null)

install-uv:
ifndef UV
	@echo "Installing uv..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
else
	@echo "uv is already installed."
endif

setup: install-uv setup-toolbox setup-terraform
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
	./terraform -chdir=python/agents/agent-adk-toolbox-cloudsql/infra init

infra-apply: setup-terraform
	@echo "Applying Terraform configuration..."
	./terraform -chdir=python/agents/agent-adk-toolbox-cloudsql/infra apply

# Run MCP Toolbox
run-toolbox: setup-toolbox
	@echo "Running MCP Toolbox..."
	./toolbox run --config python/agents/agent-adk-toolbox-cloudsql/tools.yaml

# Seed Database
seed-db: check-gcloud
	@echo "Seeding the database..."
	gcloud sql connect jobs-db-instance --user=jobs_user --project=skillful-signer-491109-r0 --quiet < python/agents/agent-adk-toolbox-cloudsql/sql/seed.sql

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
		cd python && uv run --env-file ../.env adk run agents/$(NAME); \
	fi

add-dep:
	@if [ -z "$(PKG)" ]; then \
		echo "Usage: make add-dep PKG=package_name"; \
	else \
		echo "Installing $(PKG) with uv..."; \
		cd python && uv add $(PKG); \
	fi

run-single:
	@$(MAKE) run-agent NAME=single_tool_agent

run-multi:
	@$(MAKE) run-agent NAME=multi_tool_agent

run-multimodal:
	@$(MAKE) run-agent NAME=multimodal_agent

run-rag:
	@$(MAKE) run-agent NAME=agent-adk-toolbox-cloudsql

run-team-api:
	@echo "Starting the Agent Team FastAPI server..."
	cd python && uv run uvicorn agents.agent_team.main:app --host 0.0.0.0 --port 8000 --reload

test-team-api:
	@echo "Testing the Agent Team API..."
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
