# Corporate AI Hub (Agentverse Architecture)

<img src="adk.png" width="200" alt="Agent Development Kit">

A comprehensive production-grade AI system demonstrating the full spectrum of **Multi-Agent Capabilities** using the Google Agent Development Kit (ADK) and Model Context Protocol (MCP).

## 🏗️ Grand Demo Architecture

This system follows a 5-layer model with **Zero-Trust Governance**, **Agentic RAG**, and **Cloud Run** service decoupling.

```text
                                            +---------------------------+
                                            |      USER INTERFACE       |
                                            +-------------+-------------+
                                                          |
                                                          | (Natural Language)
                                                          |
+---------------------------------------------------------v-----------------------------------------------------------+
|                                              ORCHESTRATION LAYER                                                    |
|                                         (Corporate Hub Orchestrator)                                                |
|   +--------------------------------------------------------------------------------------------------------------+  |
|   |                                   🛡️ GLOBAL GOVERNANCE GATE (Sentinel)                                        |  |
|   +-----------+--------------------------+-----------------------+------------------------+----------------------+  |
+---------------|--------------------------|-----------------------|------------------------|-------------------------+
                |                          |                       |                        |
         🧠 HYBRID MEMORY           ⚡ PARALLEL             🌳 HIERARCHICAL          🌐 REMOTE A2A
      +---------v----------+      +--------v---------+    +--------v---------+    +---------v----------+
      |   SESSION STATE    |      |   AUDIT OFFICE   |    | FINANCE DIRECTOR |    |    HR DIRECTOR     |
      | [Persistent/DB]    |      | (Legal / Policy) |    | (Treasury / Risk)|    |   (Agentic RAG)    |
      | [Ephemeral/RAM]    |      +--------+---------+    +--------+---------+    |  [DOMAIN GATE]     |
      +--------------------+               |                       |              +---------+----------+
                                           |                       |                        |
                                           |                       |               (A2A Over Network)
                                           |               +-------+-------+                |
                                           |               | (A2A Looping) |      +---------v----------+
                                           |         +-----v-----+   +-----v-----+|     CLOUD RUN      |
                                           |         | RISK AGT  |   | TREASURY  ||   (Jobs Service)   |
                                           |         +-----+-----+   +-----+-----+|   [REMOTE NODE]    |
                                           |               |               |      +---------+----------+
                                           |               |               |                |
+------------------------------------------v---------------v---------------v----------------v-------------------------+
|                                             MANAGED TOOLING (MCP)                                                   |
+--------------------------+--------------------------+---------------------------+-----------------------------------+
|       MCP TOOLBOX        |      SPANNER NATIVE      |        CUSTOM MCP         |            CUSTOM MCP             |
|      (Cloud SQL DB)      |       (Endpoints)        |        (Currency)         |             (Weather)             |
+------------+-------------+------------+-------------+-------------+-------------+-------------+---------------------+
             |                          |                           |                           |
    +--------v---------+       +--------v---------+        +--------v---------+        +--------v---------+
    |    CLOUD SQL     |       |     SPANNER      |        |     EXTERNAL     |        |    OPEN-METEO    |
    | (pgvector / RAG) |       | (Property Graph) |        |     EXCHANGE     |        |     REST API     |
    +------------------+       +------------------+        +------------------+        +------------------+
```

## 🧠 Key Capabilities Demonstrated

1.  **Remote A2A on Cloud Run**: The HR Director is decoupled into a standalone service. The Master Orchestrator discovers and delegates to it over the network using the ADK `RemoteA2aAgent` protocol.
2.  **Multi-Layer Governance (Zero Trust)**:
    *   **Global Gate**: Intercepts high-risk queries at the Orchestrator level.
    *   **Domain Gate**: The Jobs Service (on Cloud Run) has its own internal Sentinel to block unauthorized access even if called directly.
3.  **Agentic RAG**: Uses **Vertex AI Embeddings** and **Cloud SQL (pgvector)** for semantic search and intent-based retrieval.
4.  **Hybrid Memory System**: Supports both **Persistent Mode** (SQLite) for cross-session continuity and **Ephemeral Mode** (In-Memory) for privacy.
5.  **Hierarchical & Parallel Routing**: Demonstrates complex delegation including an iterative **Looping Protocol** for the Risk Analyst.

---

## 🚀 Getting Started

### 1. Setup & Environment
Install required binaries (`uv`, `terraform`, `toolbox`, `cloud-sql-proxy`) and sync Python dependencies.
```bash
make setup
make help              # See all available automation commands
```

Create a `.env` file in the root based on `.env.example`:
```bash
cp .env.example .env
```

**Configure the following in `.env`:**
- `GOOGLE_API_KEY`: Your Gemini API key from [Google AI Studio](https://aistudio.google.com/).
- `GOOGLE_CLOUD_PROJECT`: Your GCP Project ID.
- `REGION`: Your GCP region (e.g., `us-central1`).
- `DB_PASSWORD`: Set this **after** running `make infra-apply` (or use `make sync-env`).

### 2. Infrastructure & Database
Provision GCP resources, sync credentials, and seed the databases.
```bash
make infra-init        # Initialize Terraform providers
make infra-apply       # Provision GCP resources
make sync-env          # Automatically pull DB_PASSWORD into .env
make seed-db           # Seed Cloud SQL (pgvector)
make seed-spanner      # Seed Spanner Graph
```

---

## 🚀 Execution Paths

### 1. Visual Web Portal (Recommended)
Interact with the Corporate Hub using a visual chat interface.
```bash
make serve-agents      # Open http://localhost:8000
```

### 2. Local Monolith (CLI Mode)
Run everything in a single process with persistent memory.
```bash
make run-toolbox       # Terminal 1 (Required for SQL)
make run-a2a           # Terminal 2
```

### 3. Ephemeral Mode (Privacy-First)
Run without disk persistence. Memory is wiped on exit.
```bash
make run-a2a-ephemeral
```

### 4. Remote A2A (Enterprise Simulation)
Decouple the Jobs Agent into a standalone service.
```bash
make run-jobs-service  # Terminal 2 (Port 8001)
make run-a2a-remote    # Terminal 3 (Discovery Mode)
```

---

## 💡 Pro Tips

### 🛠️ Handling Experimental Warnings
When running agents, you may see `[EXPERIMENTAL]` warnings from the Google ADK library. These are expected as certain ADK features (like the Credential Service) are under active development. They do not affect functionality.

### 💰 Cost Management
Cloud SQL and Spanner can be expensive. Use these commands to pause/resume your infra:
- **Pause Everything**: `make infra-stop` (Pauses SQL + Scales down Spanner)
- **Resume Everything**: `make infra-start`

---

## 📂 Project Structure
- `python/agents/orchestrator/`: Hub Orchestrator & Global Governance.
- `python/agents/finance/`: Hierarchical domain with Looping Risk Analyst.
- `python/agents/jobs/`: HR specialist with Agentic RAG and Domain Governance.
- `python/mcp_servers/`: Standalone MCP servers wrapping external REST APIs.
- `infra/`: Terraform for Cloud SQL (pgvector) and Spanner Graph resources.
