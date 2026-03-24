# Corporate AI Hub (Agentverse Architecture)

<img src="adk.png" width="200" alt="Agent Development Kit">

A comprehensive production-grade AI system demonstrating the full spectrum of **Multi-Agent Capabilities**.

## 🏗️ Grand Demo Architecture

This system follows a 5-layer model: **User Interface** $\rightarrow$ **Orchestration** $\rightarrow$ **Hierarchical Routing** $\rightarrow$ **Specialized Protocols** $\rightarrow$ **Managed Tooling**.

```text
                                +---------------------------+
                                |      USER INTERFACE       |
                                +-------------+-------------+
                                              |
+---------------------------------------------v-----------------------------------------------+
|                                     ORCHESTRATION LAYER                                     |
|                                (Corporate Hub Orchestrator)                                 |
+------+----------------------+---------------+-----------------------+-----------------------+
       |                      |               |                       |                       |
       | (Long-Term Memory)   | (A2A - Local) | (A2A - Parallel)      | (A2A - Local)         | (A2A)
+------v--------------+  +----v----------+ +--v-----------+  +--------v-------+  +------------v---+
|  PERSISTENT STATE   |  |  HR DIRECTOR  | | AUDIT OFFICE  |  |FINANCE DIRECTOR|  |LOGISTICS AGENT |
| (SQLite Storage)    |  | (Agentic RAG) | |(Parallel Exec)|  | (Hierarchical) |  | (Custom MCP)   |
+---------------------+  +-------+-------+ +------+-------+  +--------+-------+  +-------+--------+
                                 |                |                   |                  |
                                 |                |          +--------+--------+         |
                                 |                |          | (A2A - Looping) |         |
                                 |                |    +-----v-------+  +------v-------+ |
                                 |                |    | RISK ANALYST|  |  TREASURY    | |
                                 |                |    |(Iterative)  |  | (Custom MCP) | |
                                 |                |    +------+------+  +------+-------+ |
                                 |                |           |                |         |
+--------------------------------v----------------v-----------v----------------v---------v-------+
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

## 🧠 Key Capabilities Demonstrated

1.  **Hierarchical Routing**: Master Hub $\rightarrow$ Finance Director $\rightarrow$ Risk Analyst.
2.  **Iterative Looping**: The Risk Analyst follows a strict `Gather -> Audit -> Refine` protocol.
3.  **Parallel Execution**: Simultaneous Compliance and Legal scans.
4.  **Hybrid Memory**: Persistent SQLite storage for cross-session state + Turn-based context.
5.  **Governance & Safety**: Sentinel Guardrails and Session Cooldowns.

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
