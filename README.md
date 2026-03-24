# Corporate AI Hub (Agentverse Architecture)

<img src="adk.png" width="200" alt="Agent Development Kit">

A comprehensive production-grade AI system demonstrating the full spectrum of **Multi-Agent Capabilities** using the Google Agent Development Kit (ADK) and Model Context Protocol (MCP).

## 🏗️ Grand Demo Architecture

This system follows a 5-layer model with **Zero-Trust Governance**, **Agentic RAG**, and **Hybrid Memory**.

```text
                                +---------------------------+
                                |      USER INTERFACE       |
                                +-------------+-------------+
                                              |
+---------------------------------------------v-----------------------------------------------+
|                                     ORCHESTRATION LAYER                                     |
|                                (Corporate Hub Orchestrator)                                 |
|  +---------------------------------------------------------------------------------------+  |
|  |                          🛡️ GLOBAL GOVERNANCE GATE (Sentinel)                          |  |
|  +------+----------------------+---------------+-----------------------+----------------+  |
+---------|----------------------|---------------|-----------------------|--------------------+
          |                      |               |                       |
   🧠 HYBRID MEMORY       ⚡ PARALLEL      🌳 HIERARCHICAL         🌐 REMOTE A2A
+------v--------------+  +----v----------+ +--v-----------+  +--------v-------+  +------------v---+
|   SESSION STATE     |  | AUDIT OFFICE  | |FINANCE DIRECTOR|  |  HR DIRECTOR   |  |LOGISTICS AGENT |
| [Persistent/SQLite] |  |(Legal/Policy) | | (Treasury/Risk)|  | (Agentic RAG)  |  | (External API) |
| [Ephemeral/Memory]  |  +------+-------+ +------+-------+  | [DOMAIN GATE]  |  +-------+--------+
+---------------------+         |                |          +--------+-------+          |
                                |                |                   |                  |
                                |                |          (Discovery Protocol)        |
                                |                |                   |                  |
                                |                |          +--------v--------+         |
                                |                |          |  JOBS SERVICE   |         |
                                |                |          |  (Remote A2A)   |         |
                                |                |          +--------+--------+         |
+--------------------------------v----------------v-------------------v------------------v-------+
|                                    MANAGED TOOLING (MCP)                                    |
+----------------------+----------------------+------------------------+-----------------------+
|     MCP TOOLBOX      |    SPANNER NATIVE    |      CUSTOM MCP        |      CUSTOM MCP       |
|    (Cloud SQL)       |     (Endpoints)      |      (Currency)        |       (Weather)       |
+----------+-----------+----------+-----------+-----------+------------+-----------+-----------+
           |                      |                       |                        |
+----------v----------+  +--------v-------+      +--------v-------+       +--------v-------+
|      CLOUD SQL      |  |     SPANNER    |      |    EXTERNAL    |       |    OPEN-METEO   |
| (pgvector / RAG)    |  |  (PropertyGraph)|      |   EXCHANGE     |       |    REST API     |
+---------------------+  +----------------+      +----------------+       +----------------+
```

## 🧠 Key Capabilities Demonstrated

1.  **Agentic RAG (Retrieval-Augmented Generation)**: The HR Director uses **Vertex AI Embeddings** and **Cloud SQL (pgvector)** to perform semantic search. It doesn't just look for keywords; it understands the intent behind job descriptions and candidate profiles.
2.  **Multi-Layer Governance (Zero Trust)**:
    *   **Global Gate**: Intercepts high-risk queries at the Orchestrator level.
    *   **Domain Gate**: The Jobs Service has its own internal Sentinel to block unauthorized access to sensitive HR data.
3.  **Hybrid Memory System**:
    *   **Persistent Mode**: Uses SQLite to remember user preferences across restarts.
    *   **Ephemeral Mode**: Uses In-Memory storage for privacy-first, turn-only context.
4.  **Hierarchical Routing**: Master Hub $\rightarrow$ Finance Director $\rightarrow$ Risk Analyst. Demonstrates complex organizational delegation.
5.  **Iterative Looping Protocol**: The Risk Analyst follows a strict `Gather -> Audit -> Refine` cycle until a zero-error report is produced.
6.  **Parallel Execution**: Orchestrator triggers simultaneous Compliance and Legal scans to reduce latency.
7.  **Dual-Path A2A**: Supports both **Local Monolith** (direct object calls) and **Remote Service** (network-based discovery) architectures.

---

## 🚀 Execution

### 1. Local Monolith (Standard)
Run everything in a single process with persistent memory.
```bash
make run-toolbox  # Terminal 1
make run-a2a      # Terminal 2
```

### 2. Ephemeral Mode (Privacy-First)
Run without disk persistence. Memory is wiped on exit.
```bash
make run-a2a-ephemeral
```

### 3. Remote A2A (Enterprise)
Decouple the Jobs Agent into a standalone service.
```bash
make run-jobs-service  # Terminal 2 (Port 8001)
make run-a2a-remote    # Terminal 3 (Discovery Mode)
```

---

## 📂 Project Structure
- `python/agents/orchestrator/`: Hub Orchestrator & Global Governance.
- `python/agents/finance/`: Hierarchical domain with Looping Risk Analyst.
- `python/agents/jobs/`: HR specialist with Agentic RAG and Domain Governance.
- `python/mcp_servers/`: Standalone MCP servers wrapping external REST APIs.
- `infra/`: Terraform for Cloud SQL (pgvector) and Spanner Graph resources.
