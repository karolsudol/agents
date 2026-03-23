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

---

## 🚀 Getting Started

All commands must be run from the **project root directory**.

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
# Get the password from terraform output and update .env DB_PASSWORD
make seed-db
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

## 💰 Cost Management
Cloud SQL can be expensive if left running. You can "pause" the instance when not in use:
- **Pause Instance**: `make infra-stop` (Saves CPU/Memory costs; storage still billed)
- **Resume Instance**: `make infra-start`

## 🧹 Cleanup
To avoid ongoing costs, delete all GCP resources and clean up local artifacts:
```bash
make infra-destroy
```

## 📂 Project Structure
- `infra/`: Terraform configuration for GCP resources.
- `sql/`: SQL scripts for database initialization and seeding.
- `tools.yaml`: Configuration for the MCP Toolbox bridge.
- `python/agents/`: Individual AI agent implementations.
- `deploy/`: Dockerfiles and manifests for Cloud Run deployment.

## 🛠️ Global Management
- **List agents**: `make list-agents`
- **Lint/Format**: `make lint`
- **Add Python dependency**: `make add-dep PKG=package_name`

---
*For detailed setup of specific agents (e.g. GCP Auth or API endpoints), refer to the READMEs in `python/agents/`.*
