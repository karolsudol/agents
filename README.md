# AI Agents Collection

![Agent Development Kit](agent-development-kit.png)

A collection of AI agents built with the **Agent Development Kit (ADK)** and the **Model Context Protocol (MCP)**.

## 🏗️ Architecture Overview (Agentic RAG)

```text
                  +--------------------------+
                  |          USER            |
                  +------------+-------------+
                               |
                               | (Chat UI / CLI)
                               |
                  +------------v-------------+
                  |      ADK AGENT           |
                  | (agent_toolbox_mcp)      +-------+
                  +------------+-------------+       |
                               |                     |
                               | (MCP Protocol)      | (LLM: Gemini)
                               |                     |
                  +------------v-------------+       |
                  |      MCP TOOLBOX         |       |
                  |      (tools.yaml)        |       |
                  +------+-----+-------+-----+       |
                         |     |       |             |
           +-------------+     |       +-------------v-------------+
           |                   |                     |             |
+----------v----------+ +------v-------+      +------v-------+     |
|    CLOUD SQL        | |  VERTEX AI   |      |  VERTEX AI   |     |
|   (PostgreSQL)      | | (Embeddings) |      |   (Gemini)   |     |
+---------------------+ +--------------+      +--------------+     |
           ^                   ^                     ^             |
           |                   |                     |             |
           +-------------------+---------------------+-------------+
                               |
                     (GCP Infrastructure)
```

## 📂 Project Structure

- `infra/`: Terraform configuration for GCP resources (Cloud SQL, IAM, APIs).
- `sql/`: SQL scripts for database initialization and seeding.
- `tools.yaml`: Configuration for the MCP Toolbox (DB-to-Agent bridge).
- `python/agents/`: Individual AI agent implementations.
  - [**Single Tool Agent**](./python/agents/single_tool_agent/README.md): Simple agent using a time-telling tool.
  - [**Multi Tool Agent**](./python/agents/multi_tool_agent/): Agent with both time and weather tools.
  - [**Multimodal Agent**](./python/agents/multimodal_agent/): Audio-analysis agent.
  - [**Agentic RAG (Cloud SQL)**](./python/agents/agent_toolbox_mcp/README.md): Advanced RAG using MCP Toolbox.
  - [**Agent Team**](./python/agents/agent_team/README.md): Multi-agent orchestration via FastAPI.

## 🚀 Quick Start (Root Commands)

### 1. Setup
Install all required binaries (`uv`, `terraform`, `toolbox`, `cloud-sql-proxy`) and sync Python dependencies.
```bash
make setup
```

### 2. Infrastructure & Database
Provision GCP resources and seed the database.
```bash
make infra-init
make infra-apply
make seed-db
```

### 3. Run Agents
- **Agentic RAG**:
  ```bash
  make run-toolbox  # Terminal 1
  make run-rag      # Terminal 2
  ```
- **Single Tool Agent**: `make run-single`
- **Multi Tool Agent**: `make run-multi`
- **Multimodal Agent**: `make run-multimodal`

## 🛠️ Global Management
- **List agents**: `make list-agents`
- **Serve Web UI**: `make serve-agents`
- **Lint/Format**: `make lint`
- **Add Python dependency**: `make add-dep PKG=package_name`

---
*For detailed setup of specific agents (e.g. GCP Auth or API endpoints), refer to the READMEs in `python/agents/`.*
