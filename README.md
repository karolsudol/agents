# agents
![Agent Development Kit](agent-development-kit.png)

Sample agents demo: A2A + ADK + MCP + RAG + Clean multi-lang structure.

## Setup
1.  **Environment Setup**:
    ```bash
    make setup
    make install-precommit
    ```
2.  **API Key**:
    Copy `.env.example` to `.env` at the root and add your `GOOGLE_API_KEY`. This key will be shared by both Python and Go agents.
    ```bash
    cp .env.example .env
    ```

## Managing Agents
- **List all agents**: `make list-agents`
- **Run Single Tool Agent**: `make run-single`
- **Run Multi Tool Agent**: `make run-multi`
- **Run Multimodal Agent**: `make run-multimodal`
- **Serve Web UI**: `make serve-agents`
- **Add a Python dependency**: `make add-dep PKG=requests`

To activate the virtual environment:
```bash
# Get the activation command
make activate
# OR drop into a subshell
make shell
```

## Structure
- `python/agents`: Python-based AI agents (ADK).
  - `single_tool_agent`: Simple agent using a time-telling tool.
  - `multi_tool_agent`: Agent with both time and weather tools.
  - `multimodal_agent`: Multimodal agent with an audio-analysis tool.
- `python/notebooks`: Colab notebooks.
- `go/agents`: Go-based AI agents.
