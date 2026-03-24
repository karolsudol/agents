# Corporate AI Hub (Agentverse Architecture)

<img src="adk.png" width="200" alt="Agent Development Kit">

A production-grade collection of AI agents following the **Agentverse Architect** model. This system manages corporate operations across HR, Finance, and Logistics using **Agent-to-Agent (A2A)** orchestration, **Model Context Protocol (MCP)**, and **Long-Term Memory**.

## 🏗️ Architecture Overview

The system is structured into four layers: **Orchestration**, **Domain Workflows**, **Managed Tooling**, and **Persistent Storage**.

```text
                                +---------------------------+
                                |      USER INTERFACE       |
                                +-------------+-------------+
                                              |
                                              | (Natural Language)
                                              |
+---------------------------------------------v-----------------------------------------------+
|                                     ORCHESTRATION LAYER                                     |
|                                (Corporate Hub Orchestrator)                                 |
+------+----------------------+---------------+-----------------------+-----------------------+
       |                      |               |                       |                       |
       | (Long-Term Memory)   | (A2A)         | (A2A - Looping)       | (A2A - Parallel)      | (A2A)
+------v--------------+  +----v----------+ +--v-----------+  +--------v-------+  +------------v---+
|  PERSISTENT STATE   |  | HR/RECRUITMENT| | RISK ANALYST  |  |  COMPLIANCE    |  | TREASURY/FX    |
| (JSON/Local File)   |  | (Agentic RAG) | |(Iterative Loop)|  | (Parallel Scan)|  | (Custom MCP)   |
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
```

## 🧠 Key Agentverse Patterns

1.  **Orchestration & Safety**: The **Sentinel Guardrail** intercepts high-risk queries, while the **CoolDown Plugin** prevents system overload.
2.  **Long-Term Memory**: The `PersistentSessionService` ensures the hub remembers user preferences and context across restarts by storing state in `sessions_storage.json`.
3.  **Looping Protocol (Risk Analyst)**: The Risk agent follows a `Gather -> Audit -> Refine` loop, ensuring zero-error financial reports.
4.  **Parallel Execution (Compliance)**: The Orchestrator can trigger compliance and risk scans simultaneously to provide a comprehensive corporate audit.
5.  **Agentic RAG**: The HR Agent uses Vertex AI Embeddings and pgvector to semantically match candidates to job descriptions.

---

## 🚀 Execution

### Local Development
- **Start All Services**:
  - Terminal 1: `make run-toolbox` (Required for Cloud SQL features)
  - Terminal 2: `make run-a2a` (Starts the Corporate Hub)
- **Web UI**: `make serve-agents` (Interact at http://localhost:8000)

### Production Deployment
```bash
make deploy-toolbox
make deploy-agent
```

---

## 📂 Project Structure
- `python/agents/orchestrator/`: Hub Orchestrator, Sentinel, and Governance Plugins.
- `python/agents/finance/`: Risk Analyst (Looping) and Compliance (Parallel).
- `python/agents/jobs/`: HR specialist using Agentic RAG.
- `python/mcp_servers/`: Custom MCP implementations for Currency and Weather APIs.
