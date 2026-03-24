# AI Agents Collection

<img src="adk.png" width="200" alt="Agent Development Kit">

A collection of AI agents built with the **Agent Development Kit (ADK)**, the **Model Context Protocol (MCP)**, and **Retrieval-Augmented Generation (RAG)**.

## 🏗️ Agentverse Architecture

Following the **Agentverse** model, this repository is structured into distinct layers of responsibility: **Orchestration**, **Domain Workflows**, and **Managed Tools**.

```text
                                +---------------------------+
                                |      USER INTERFACE       |
                                +-------------+-------------+
                                              |
                                              | (Natural Language)
                                              |
+---------------------------------------------v-----------------------------------------------+
|                                     ORCHESTRATION LAYER                                     |
|                                    (Master Orchestrator)                                    |
+------+----------------------+---------------+-----------------------+-----------------------+
       |                      |               |                       |                       |
       | (State/Memory)       | (A2A)         | (A2A)                 | (A2A)                 | (A2A)
+------v--------------+  +----v----------+ +--v-----------+  +--------v-------+  +------------v---+
|   SESSION MEMORY    |  |  JOBS DOMAIN  | | FINANCE DOMAIN |  | CURRENCY DOMAIN|  | WEATHER DOMAIN |
| (InMemory/Database) |  | (Agentic RAG) | | (Graph/Spanner)|  |  (Custom MCP)  |  |  (Custom MCP)  |
+---------------------+  +-------+-------+ +------+-------+  +--------+-------+  +-------+--------+
                                 |                |                   |                  |
+--------------------------------v----------------v-------------------v------------------v-------+
|                                    MANAGED TOOLING (MCP)                                    |
+----------------------+----------------------+------------------------+-----------------------+
|     MCP TOOLBOX      |    SPANNER NATIVE    |      CUSTOM MCP        |      CUSTOM MCP       |
|    (Cloud SQL)       |     (Endpoints)      |      (Currency)        |       (Weather)       |
+----------+-----------+----------+-----------+-----------+------------+-----------+-----------+
           |                      |                       |                        |
+----------v----------+  +--------v-------+      +--------v-------+       +--------v-------+
|      CLOUD SQL      |  |     SPANNER    |      |    EXTERNAL    |       |    OPEN-METEO   |
|     (PostgreSQL)    |  |  (PropertyGraph)|      |   EXCHANGE     |       |    REST API     |
+---------------------+  +----------------+      +----------------+       +----------------+
           |                      |                       |                        |
           +----------------------+-----------+-----------+------------------------+
                                              |
                                    (GCP Infrastructure)
```

## 🔍 Architecture Layers

1.  **Orchestration Layer**: The "Brain" that manages the conversation flow. It uses **Agent-to-Agent (A2A)** calls to delegate to specialized domains.
2.  **Domain Workflows**: Specialist agents (Jobs, Spanner, Currency, Weather) that have deep knowledge of their specific domain and available tools.
3.  **Managed Tooling (MCP)**: The standardized communication layer. Whether it's a native Google service or a custom REST wrapper, everything speaks MCP.
4.  **Session Memory**: Manages state across turns, ensuring the Orchestrator remembers user preferences (like temperature units or job interests).

---

## 🚀 Getting Started

### 1. Setup & Environment
Install required binaries (`uv`, `terraform`, `toolbox`, `cloud-sql-proxy`) and sync Python dependencies.
```bash
make setup
```

### 2. Infrastructure & Database
Provision GCP resources and seed the databases.
```bash
make infra-init
make infra-apply
make seed-db       # Seed Cloud SQL
make seed-spanner  # Seed Spanner Graph
```

### 3. Execution

#### Local Development
- **Master Orchestrator (A2A)**:
  - Terminal 1: `make run-toolbox` (Middleware for SQL)
  - Terminal 2: `make run-a2a` (Orchestrator that coordinates all domains)
- **Web UI**: `make serve-agents` (Visual interface at http://localhost:8000)

#### Cloud Deployment
```bash
make deploy-toolbox
make deploy-agent
```

---

## 📂 Project Structure
- `python/agents/orchestrator/`: Master coordinator (The "Brain").
- `python/agents/[domain]/`: Specialist domain agents (Jobs, Spanner, etc.).
- `python/mcp_servers/`: Custom MCP implementations for REST APIs and logic.
- `infra/`: Terraform for all GCP resources.
