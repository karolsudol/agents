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
       | (Long-Term Memory)   | (A2A)         | (A2A - Parallel)      | (A2A)                 | (A2A)
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

1.  **Hierarchical Routing**: The `Orchestrator` delegates to the `Finance Director`, who further routes requests to `Risk` or `Treasury`. This multi-level hierarchy mimics real corporate structures.
2.  **Iterative Looping Agent**: The `Risk Analyst` follows a strict `Gather -> Audit -> Refine` protocol, ensuring reports are perfect before reaching the user.
3.  **Parallel Execution**: The `Audit Office` runs `Compliance` and `Legal` scans simultaneously, significantly reducing latency for multi-factor validations.
4.  **Hybrid Memory System**:
    *   **Short-Term Memory**: ADK `Context` tracks conversation history and user intent within the current turn.
    *   **Long-Term Memory**: Persistent `SqliteSessionService` stores user state (e.g., "preferred currency: EUR") across days and restarts.
5.  **Agentic RAG**: The `HR Agent` performs semantic vector search using Vertex AI and Cloud SQL `pgvector`.

---

## 🚀 Execution

### Local Development
- **Start Stack**:
  - Terminal 1: `make run-toolbox` (Required for Cloud SQL)
  - Terminal 2: `make run-a2a` (Starts the Orchestrator)
- **Web UI**: `make serve-agents` (Visual interface at http://localhost:8000)

### Production Deployment
```bash
make deploy-toolbox
make deploy-agent
```
