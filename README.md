# AI Agents Hub (Next-Gen Protocols)

<img src="adk.png" width="200" alt="Agent Development Kit">

Multi-agent architecture implementing the following industry standards:
- **OWS / AP2**: Decentralized Identity & Transaction Signing
- **Solana x402**: Autonomous HTTP 402 Payments
- **UCP**: Universal Commerce Protocol (Quotes/Orders)
- **A2A**: Agent-to-Agent Service Discovery
- **A2UI**: Structured Interface Widgets (Charts/Forms)
- **AG-UI**: Standardized SSE Streaming Middleware
- **MCP**: Model Context Protocol for Tooling

## 🏗️ Architecture

This system uses a **Core Coordinator** to manage specialized hubs for **Payments** and **HR**, integrating native cryptographic identities and commerce schemas.

```text
                                            +---------------------------+
                                            |      USER INTERFACE       |
                                            |   (A2UI / AG-UI Stream)   |
                                            +-------------+-------------+
                                                          |
                                            +-------------v-------------+
                                            |     CORE COORDINATOR      |
                                            |   (Global Governance)     |
                                            +-------------+-------------+
                                                          |
                 +----------------------------------------+-----------------------------------------+
                 |                                                                                  |
      [ 💳 PAYMENTS HUB ]                                                                   [ 🏢 HR HUB ]
 (Finance / Treasury / Risk)                                                           (Jobs / Hiring / RAG)
                 |                                                                                  |
 +---------------+---------------+                                                  +---------------+---------------+
 |      🛡️ IDENTITY (OWS)        |                                                  |    🌐 REMOTE A2A (ADK)        |
 | (Self-Sovereign Identity)     |                                                  |   (Service Discovery)         |
 +---------------+---------------+                                                  +---------------+---------------+
 |      💰 COMMERCE (x402)       |                                                  |    🧠 AGENTIC RAG             |
 | (Solana Micropayments)        |                                                  |   (Cloud SQL / pgvector)      |
 +---------------+---------------+                                                  +---------------+---------------+
                 |                                                                                  |
 +--------------------------------------------------------------------------------------------------+---------------+
 |                                         MANAGED TOOLING (MCP)                                                    |
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

## 🧠 Protocol Details

1.  **Identity (OWS/AP2)**: Agents sign actions using decentralized identities (DIDs) via the **OpenWallet SDK**.
2.  **Commerce (Solana x402 / UCP)**:
    *   **x402**: Automated `HTTP 402` payment negotiation for tool access.
    *   **UCP**: Standardized procurement lifecycle with unified request/response schemas.
3.  **Discovery (A2A / Agent Cards)**: Dynamic discovery via `/.well-known/agent-card.json`.
4.  **Interface (A2UI / AG-UI)**:
    *   **A2UI**: Emits structured UI metadata for charts and forms.
    *   **AG-UI**: Standardized Event Stream for text, tool calls, and lifecycle events.
5.  **Agentic RAG**: HR Hub uses **Vertex AI Embeddings** and **pgvector** for domain-specific retrieval.

---

## 🚀 Getting Started

### 1. Setup & Environment
Install binaries (`uv`, `terraform`, `toolbox`) and sync dependencies.
```bash
make setup
make help              # See all available automation commands
```

**Configure the following in `.env`:**
- `GOOGLE_API_KEY`: Your Gemini API key.
- `SOLANA_RPC_URL`: Endpoint for x402 settlement.
- `OWS_WALLET_PASSPHRASE`: Passphrase for Agent Identity encryption.

### 2. Infrastructure & Database
Provision resources and seed the databases.
```bash
make infra-init
make infra-apply
make seed-db
make seed-spanner
```

---

## 📂 Project Structure
- `python/agents/orchestrator/`: Core Coordinator & Global Sentinel.
- `python/agents/identity/`: OWS Wallet & AP2 Mandate management.
- `python/agents/finance/`: Payments Hub with x402 and UCP tools.
- `python/agents/jobs/`: HR Hub with Remote A2A and RAG.
- `python/mcp_servers/`: MCP servers wrapping external REST APIs.
- `infra/`: Terraform for Cloud SQL (pgvector) and Spanner Graph.
