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

1.  **It is an MCP Server**: It follows the [Model Context Protocol](https://modelcontextprotocol.io), a standard that allows any AI to connect to data sources.
2.  **No-Code Tools**: You define your SQL queries and their parameters in `tools.yaml`.
3.  **LLM Independent**: The Toolbox doesn't care which LLM you use (Gemini, Claude, GPT, etc.).

## 🔍 Understanding Embeddings & Cloud SQL

This project uses **In-Database Embeddings** to power semantic search for job listings.

### What are Embeddings?
Embeddings are numerical representations (vectors) of text that capture its meaning. Instead of searching for exact words (keyword search), we search for "nearby" concepts (semantic search).
- **Model**: We use Google's `text-embedding-004`.
- **Dimension**: Each text is converted into a **3072-dimensional** vector.

### How Cloud SQL Integrates with AI
We use the **`google_ml_integration`** extension and the **`pgvector`** extension in Cloud SQL PostgreSQL to:
1.  **Generate Vectors**: Call Vertex AI directly from SQL using the `embedding()` function.
2.  **Store Vectors**: Store these embeddings in a `vector(3072)` column.
3.  **Semantic Search**: Use the `<=>` operator (cosine distance) to find the most relevant jobs based on a user's description.

## 📂 Project Structure

- `infra/`: Terraform configuration for GCP resources (Cloud SQL, Spanner, IAM, APIs).
- `sql/`: SQL scripts for database initialization and seeding.
- `tools.yaml`: Configuration for the MCP Toolbox bridge.
- `python/agents/`: Individual AI agent implementations.
  - [**Single Tool Agent**](./python/agents/single_tool_agent/README.md): Simple agent using a time-telling tool.
  - [**Multi Tool Agent**](./python/agents/multi_tool_agent/): Agent with both time and weather tools.
  - [**Multimodal Agent**](./python/agents/multimodal_agent/): Audio-analysis agent.
  - [**Agentic RAG (Cloud SQL)**](./python/agents/agent_toolbox_mcp/README.md): Advanced RAG using MCP Toolbox.
  - [**Spanner Graph MCP**](#spanner-graph-mcp): Fraud detection using Spanner Property Graphs and MCP.
  - [**Agent Team**](./python/agents/agent_team/README.md): Multi-agent orchestration via FastAPI.

## 🚀 Quick Start (Root Commands)

### 1. Setup & Environment
Install required binaries (`uv`, `terraform`, `toolbox`, `cloud-sql-proxy`) and sync Python dependencies.
```bash
make setup
```
Create a `.env` file in the root based on `.env.example` and set your `GOOGLE_CLOUD_PROJECT`.

### 2. Infrastructure & Database
Provision GCP resources and seed the database.
```bash
make infra-init
make infra-apply
# Update .env DB_PASSWORD with the terraform output
make seed-db
make seed-spanner
```

### 3. Choose Your Execution Path

#### Option A: Local Development
Run the stack on your local machine.
- **Terminal 1**: `make run-toolbox` (Starts the MCP Server)
- **Terminal 2**: `make run-rag` (Starts the AI Agent)
- **Web UI**: `make serve-agents` (Interact with all agents via browser at http://localhost:8000)

#### Option B: Cloud Deployment (Cloud Run)
Deploy the services to Google Cloud for public access.
```bash
make deploy-toolbox
make deploy-agent
```

---

## 🏦 Spanner Graph MCP
This feature uses **Cloud Spanner's Property Graph** capabilities to perform fraud detection and relationship analysis.

### Setup
The infrastructure and seeding are covered in the **Quick Start** section. The Spanner MCP is configured globally via `.gemini/settings.json`.

### Usage (via Gemini CLI)
You can interact with your Spanner graph using natural language:
```bash
gemini "Show me all transfers from Karol to John"
gemini "Identify potential circular transfer patterns for fraud detection"
```

---

## 💰 Cost Management
Cloud SQL and Spanner can be expensive. You can "pause" the Cloud SQL instance when not in use:
- **Pause Instance**: `make infra-stop`
- **Resume Instance**: `make infra-start`

## 🧹 Cleanup
To delete all GCP resources (Cloud SQL, Spanner, etc.) and clean up local artifacts:
```bash
make infra-destroy
```

## 🛠️ Global Management
- **List agents**: `make list-agents`
- **Lint/Format**: `make lint`
- **Add Python dependency**: `make add-dep PKG=package_name`

---
*For detailed setup of specific agents (e.g. GCP Auth or API endpoints), refer to the READMEs in `python/agents/`.*
