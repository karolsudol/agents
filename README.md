# AI Agents Collection

![Agent Development Kit](agent-development-kit.png)

A collection of AI agents built with the **Agent Development Kit (ADK)**, the **Model Context Protocol (MCP)**, and **Retrieval-Augmented Generation (RAG)**.

## 🏗️ Architecture Overview

This repository demonstrates how AI Agents connect to diverse data sources using the **Model Context Protocol (MCP)**.

```text
                  +--------------------------+
                  |          USER            |
                  +------------+-------------+
                               |
                               | (Natural Language)
                               |
                  +------------v-------------+      +-----------------------+
                  |      ADK AGENT           |      |      ANY LLM          |
                  |  (agent_toolbox_mcp)     <------> (Gemini, Claude, etc) |
                  |  (agent_spanner_mcp)     |      +-----------+-----------+
                  +------------+-------------+                  |
                               |                                |
                               | (MCP Protocol)                 |
                               |                                |
                  +------------v-------------+                  |
                  |      MCP SERVER          |                  |
                  |  (Toolbox / Spanner)     |                  |
                  +------+-----+-------+-----+                  |
                         |     |       |                        |
           +-------------+     |       +-------------+----------+
           |                   |                     |
+----------v----------+ +------v-------+      +------v-------+
|    CLOUD SQL        | |  VERTEX AI   |      |   SPANNER    |
|   (PostgreSQL)      | | (Embeddings) |      | (Graph/MCP)  |
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

This project uses **In-Database Embeddings** to power semantic search for job listings in Cloud SQL. We use the **`google_ml_integration`** and **`pgvector`** extensions to store and query 3072-dimensional vectors.

## 🏦 Spanner Graph MCP

The **Spanner Graph Agent** uses Cloud Spanner's **Property Graph** capabilities to perform fraud detection and relationship analysis.

1.  **Property Graphs**: We model financial entities (Accounts, Persons) and their relationships (Owns, Transfers) as a graph.
2.  **Native MCP**: Unlike Cloud SQL which uses the Toolbox, Cloud Spanner provides a **native MCP endpoint** (`/mcp`) that agents can connect to directly.

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
Provision GCP resources and seed the databases.
```bash
make infra-init
make infra-apply
# Update .env DB_PASSWORD with the terraform output
make seed-db       # Seed Cloud SQL
make seed-spanner  # Seed Spanner Graph
```

### 3. Choose Your Execution Path

#### Option A: Local Development
Run the stack on your local machine.
- **Agentic RAG (Cloud SQL)**:
  - Terminal 1: `make run-toolbox`
  - Terminal 2: `make run-rag`
- **Spanner Graph Agent**:
  - Terminal 1: `make run-spanner`
- **Web UI**: `make serve-agents` (Interact with all agents at http://localhost:8000)

#### Option B: Cloud Deployment (Cloud Run)
Deploy the Cloud SQL stack to Google Cloud.
```bash
make deploy-toolbox
make deploy-agent
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

## 📂 Project Structure
- `infra/`: Terraform configuration for GCP resources.
- `sql/`: SQL scripts for database initialization and seeding (`cloud_sql_seed.sql`, `spanner_seed.sql`).
- `tools.yaml`: Configuration for the MCP Toolbox bridge.
- `python/agents/`: Individual AI agent implementations.
- `deploy/`: Dockerfiles and manifests for Cloud Run deployment.

---
*For detailed setup of specific agents (e.g. GCP Auth or API endpoints), refer to the READMEs in `python/agents/`.*
