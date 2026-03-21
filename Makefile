.PHONY: install setup install-precommit lint activate shell

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

lint:
	cd python && uv run ruff check . --fix
	cd python && uv run ruff format .

