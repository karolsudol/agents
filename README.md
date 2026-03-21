# agents
Sample agents demo: A2A + ADK + MCP + RAG + Clean multi-lang structure.

## Python Setup
We use `uv` for Python dependency management.
To set up the environment and pre-commit hooks, run:
```bash
make setup
make install-precommit
```

To activate the virtual environment:
```bash
# Get the activation command
make activate
# OR drop into a subshell
make shell
```

## Structure
- `python/agents`: Python-based AI agents.
- `python/notebooks`: Colab notebooks.
- `go/agents`: Go-based AI agents.

