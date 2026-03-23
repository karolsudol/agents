# AI Agents Collection

![Agent Development Kit](agent-development-kit.png)

A collection of AI agents built with the **Agent Development Kit (ADK)**, the **Model Context Protocol (MCP)**, and **Retrieval-Augmented Generation (RAG)**.

## 🏗️ Architecture Overview (Agentic RAG)

The core of this repository is the **Agentic RAG** pattern, which connects an AI Agent to a database using the **Model Context Protocol (MCP)**.

```text
                  +--------------------------+
                  |          USER            |
                  +------------+-------------+
                               |
                               | (Natural Language)
                               |
                  +------------v-------------+      +-----------------------+
                  |      ADK AGENT           |      |      ANY LLM          |
                  | (agent_toolbox_mcp)      <------> (Gemini, Claude, etc) |
                  +------------+-------------+      +-----------+-----------+
                               |                                |
                               | (MCP Protocol)                 |
                               |                                |
                  +------------v-------------+                  |
                  |      MCP TOOLBOX         |                  |
                  |  (The DB-to-AI Bridge)   |                  |
                  +------+-----+-------+-----+                  |
                         |     |       |                        |
           +-------------+     |       +-------------+----------+
           |                   |                     |
+----------v----------+ +------v-------+      +------v-------+
|    CLOUD SQL        | |  VERTEX AI   |      |  VERTEX AI   |
|   (PostgreSQL)      | | (Embeddings) |      |   (Gemini)   |
+---------------------+ +--------------+      +--------------+
           ^                   ^                     ^
           |                   |                     |
           +-------------------+---------------------+
                               |
                     (GCP Infrastructure)
```

## 🧠 What is the MCP Toolbox?

The **MCP Toolbox for Databases** is a standalone server (middleware) that translates your database into a set of tools that an AI can understand.

1.  **It is an MCP Server**: It follows the [Model Context Protocol](https://modelcontextprotocol.io), a standard that allows any AI (like your ADK Agent, Claude Desktop, or a custom UI) to connect to data sources.
2.  **No-Code Tools**: You define your SQL queries and their parameters in `tools.yaml`. The Toolbox automatically turns these into "Tools" with names and descriptions.
3.  **The Middleman**: When the Agent needs to find a job, it sends a request to the Toolbox. The Toolbox runs the SQL, handles the connection to Cloud SQL, and returns the results to the Agent.
4.  **LLM Independent**: While this demo uses Gemini on Vertex AI, the **MCP Toolbox doesn't care which LLM you use**. You can point a Claude or GPT-based agent at the same Toolbox and it will work perfectly.

## 📂 Project Structure

- `infra/`: Terraform configuration for GCP resources (Cloud SQL, IAM, APIs).
- `sql/`: SQL scripts for database initialization and seeding.
- `tools.yaml`: Configuration for the MCP Toolbox (The bridge definitions).
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
  make run-toolbox  # Terminal 1: Starts the MCP Server
  make run-rag      # Terminal 2: Starts the AI Agent
  ```

---
*For detailed setup of specific agents (e.g. GCP Auth or API endpoints), refer to the READMEs in `python/agents/`.*
