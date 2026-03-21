# Python Agents Repository
This directory contains all the Python-based AI agent samples and related code.

## Structure
- `agents/`: Individual AI agent implementations (ADK).
  - `time_teller/`: Example agent using a tool to tell the time.
- `notebooks/`: Jupyter/Colab notebooks for experimentation.

## Setup
We use `uv` for modern Python package management.
```bash
cd ..
make setup
```

## Tools and Quality
We use **Ruff** for fast linting and formatting, and **mypy** for type checking.
To run all checks:
```bash
make lint
```
