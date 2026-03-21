.PHONY: install setup install-precommit lint activate shell run-demo serve-demo list-agents run-agent add-dep

UV := $(shell command -v uv 2> /dev/null)

install-uv:
ifndef UV
	@echo "Installing uv..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
else
	@echo "uv is already installed."
endif

setup: install-uv
	@echo "Setting up Python environment..."
	cd python && uv sync

install-precommit: setup
	@echo "Installing pre-commit hooks..."
	cd python && uv run pre-commit install

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
		cd python && uv run adk run agents/$(NAME); \
	fi

add-dep:
	@if [ -z "$(PKG)" ]; then \
		echo "Usage: make add-dep PKG=package_name"; \
	else \
		echo "Installing $(PKG) with uv..."; \
		cd python && uv add $(PKG); \
	fi

run-demo:
	@$(MAKE) run-agent NAME=time_teller

serve-demo:
	@echo "Serving the time_teller agent web interface on port 8000..."
	cd python && uv run adk web agents/time_teller --port 8000

lint:
	cd python && uv run ruff check . --fix
	cd python && uv run ruff format .
	cd python && uv run mypy .



