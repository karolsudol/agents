# AI Agents Hub (Next-Gen Protocols)

<img src="adk.png" width="200" alt="Agent Development Kit">

A production-grade AI system demonstrating **Multi-Agent Capabilities** using the Google Agent Development Kit (ADK), Model Context Protocol (MCP), Solana x402, and OpenWallet Standard (OWS).

## 🏗️ Architecture (Multi-Protocol)

This system follows a modular architecture where a **Core Coordinator** manages specialized hubs. It integrates **OWS Identity**, **x402 Payments**, and **A2A Discovery**.

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

## 🧠 Protocol Capabilities

1.  **Identity (OWS/AP2)**: Every agent has a cryptographic wallet managed via the **OpenWallet SDK**. Actions are signed using decentralized identities (DIDs).
2.  **Commerce (Solana x402)**: Implements `HTTP 402` for agent-to-agent transactions. The Payments Hub settles micropayments for API resources on Solana.
3.  **Discovery (A2A / Agent Cards)**: Agents expose a `/.well-known/agent-card.json` for dynamic discovery. The Core Coordinator uses this to route requests without hardcoding.
4.  **Interface (A2UI)**: Structured UI streaming. Agents send interactive cards (Forms, Charts, Approvals) instead of just raw text.
5.  **Agentic RAG**: Decoupled HR Hub uses **Vertex AI Embeddings** and **pgvector** for domain-specific knowledge retrieval.

---

## 🚀 Getting Started

### 1. Setup & Environment
Install required binaries (`uv`, `terraform`, `toolbox`, `cloud-sql-proxy`) and sync Python dependencies.
```bash
make setup
make help              # See all available automation commands
```

**Configure the following in `.env`:**
- `GOOGLE_API_KEY`: Your Gemini API key.
- `SOLANA_RPC_URL`: Endpoint for x402 settlement (e.g., Helius/QuickNode).
- `OWS_WALLET_KEY`: Encrypted seed for Agent Identity.

### 2. Infrastructure & Database
Provision GCP resources and seed the databases.
```bash
make infra-init
make infra-apply
make seed-db
make seed-spanner
```

---

## 📂 Project Structure
- `python/agents/orchestrator/`: Core Coordinator & Global Sentinel.
- `python/agents/identity/`: **NEW** OWS Wallet & AP2 Mandate management.
- `python/agents/finance/`: Payments Hub with x402 payment hooks.
- `python/agents/jobs/`: HR Hub with Remote A2A and Domain Governance.
- `python/mcp_servers/`: MCP servers wrapping external REST APIs.
- `infra/`: Terraform for Cloud SQL (pgvector) and Spanner Graph.
