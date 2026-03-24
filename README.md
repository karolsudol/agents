# AI Agents Collection

![Agent Development Kit](agent-development-kit.png)

A collection of AI agents built with the **Agent Development Kit (ADK)**, the **Model Context Protocol (MCP)**, and **Retrieval-Augmented Generation (RAG)**.

## 🏗️ Architecture Overview

This repository demonstrates three ways AI Agents connect to data sources and collaborate using the **Model Context Protocol (MCP)** and **Agent-to-Agent (A2A)** orchestration.

```text
                  +--------------------------+
                  |          USER            |
                  +------------+-------------+
                               |
                               | (Natural Language)
                               |
                  +------------v-------------+      +-----------------------+
                  |    TEAM ORCHESTRATOR     |      |      ANY LLM          |
                  |     (Super Agent)        <------> (Gemini, Claude, etc) |
                  +------------+-------------+      +-----------+-----------+
                               |
                +--------------+--------------+
                |              |              |
         (A2A)  |       (A2A)  |       (A2A)  |
      +---------v-----+  +-----v-------+  +---v-----------+
      |  JOBS AGENT   |  | SPANNER AGT |  | CURRENCY AGT  |
      +---------+-----+  +-----+-------+  +---+-----------+
                |              |              |
                |              |              |
         +------v-------+      |       +------v-------+
         | MCP TOOLBOX  |      |       |  CUSTOM MCP  |
         | (Middleware) |      |       |   (Server)   |
         +------+-------+      |       +--------------+
                |              |
  +-------------+              +-------------+-----------+
  |                                          |           |
+-v---------+ +--------------+         +-----v--------+  |
| CLOUD SQL | |  VERTEX AI   |         |   SPANNER    |  |
| (Postgre) | | (Embeddings) |         | (Native MCP) |  |
+-----------+ +--------------+         +--------------+  |
      ^              ^                        ^          |
      |              |                        |          |
      +--------------+-----------+------------+----------+
                                 |
                       (GCP Infrastructure)
```

## 🧠 Why is Spanner different from Cloud SQL?

There are three patterns used in this project:

1.  **Middleware Pattern (Cloud SQL)**: Standard databases like PostgreSQL don't speak MCP. We run the **MCP Toolbox** as a standalone server. It acts as a translator: Agent ↔ MCP Toolbox ↔ Cloud SQL.
2.  **Native Pattern (Spanner)**: Cloud Spanner has **built-in MCP support**. It provides a native endpoint (`/mcp`) that Google manages for you. The Agent talks directly to the database service without needing any extra middleware or "toolbox" binary.
3.  **Custom Server Pattern (Currency)**: We built a custom Python-based MCP server that provides specialized financial tools. The Agent connects via Stdio or SSE.

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
Run the full A2A stack or individual agents.
- **Master Orchestrator (A2A)**:
  - Terminal 1: `make run-toolbox` (Middleware for SQL)
  - Terminal 2: `make run-a2a` (Orchestrator that calls all other agents)
- **Specialized Agents**:
  - `make run-jobs` (Jobs Agent only)
  - `make run-spanner` (Spanner Graph Agent only)
  - `make run-currency` (Currency Agent only)
- **Web UI**: `make serve-agents` (Interact with all agents at http://localhost:8000)

#### Option B: Cloud Deployment (Cloud Run)
Deploy the stack to Google Cloud.
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
- `tools.yaml`: Configuration for the MCP Toolbox bridge (Cloud SQL only).
- `python/agents/`: Individual AI agent implementations.
- `deploy/`: Dockerfiles and manifests for Cloud Run deployment.

---
*For detailed setup of specific agents (e.g. GCP Auth or API endpoints), refer to the READMEs in `python/agents/`.*
