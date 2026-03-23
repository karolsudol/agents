# Python Agents Repository

This directory contains Python-based AI agent samples developed using the **Agent Development Kit (ADK)** and the **Model Context Protocol (MCP)**.

## Structure

- `agents/`: Individual AI agent implementations. Each directory contains its own `README.md` with specific setup and usage instructions.
  - [**Single Tool Agent**](./agents/single_tool_agent/README.md): Simple agent using a time-telling tool.
  - [**Multi Tool Agent**](./agents/multi_tool_agent/): Agent with both time and weather tools.
  - [**Multimodal Agent**](./agents/multimodal_agent/): Multimodal agent with an audio-analysis tool.
  - [**Agentic RAG (Cloud SQL)**](./agents/agent_adk_toolbox_cloudsql/README.md): Advanced RAG agent using MCP Toolbox and Cloud SQL.
  - [**Agent Team**](./agents/agent_team/README.md): Multi-agent orchestration with a FastAPI server.
- `notebooks/`: Jupyter/Colab notebooks for experimentation.

## Global Management

Most tasks are managed via the **root `Makefile`** to ensure consistent environments.

### General Setup
```bash
make setup
```

### Listing Agents
```bash
make list-agents
```

### Running Specific Agents
If you want to run an agent using global defaults:
```bash
make run-agent NAME=agent_directory_name
```
Or use the pre-defined shortcuts:
- `make run-single`
- `make run-multi`
- `make run-multimodal`
- `make run-rag`

### Quality Control
Run linting, formatting, and type checks across all Python code:
```bash
make lint
```

## Local Development
For detailed instructions on a specific agent (e.g., infrastructure setup for RAG or API endpoints for the Agent Team), please refer to the `README.md` inside that agent's directory.
