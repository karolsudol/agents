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
- **Run a specific agent**: `make run-agent NAME=intro_demo`
- **Add a Python dependency**: `make add-dep PKG=requests`

To activate the virtual environment:
```bash
# Get the activation command
make activate
# OR drop into a subshell
make shell
```


## Running the ADK Demo Agent
1. Add your `GOOGLE_API_KEY` to `python/agents/intro_demo/.env`.
2. Run the agent in the CLI:
   ```bash
   make run-demo
   ```
3. Or launch the web interface:
   ```bash
   make serve-demo
   ```

## Structure
- `python/agents`: Python-based AI agents (ADK).
  - `intro_demo`: A sample agent using ADK with a time-telling tool.
- `python/notebooks`: Colab notebooks.
- `go/agents`: Go-based AI agents.


