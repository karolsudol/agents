# Agentic RAG with MCP Toolbox for Databases

This agent uses the **MCP Toolbox for Databases** to bridge a Gemini-powered agent with **Cloud SQL (PostgreSQL)**.

## Project Structure

- `infra/`: Terraform configuration for GCP resources.
- `sql/seed.sql`: SQL script to initialize the database and seed it with jobs.
- `tools.yaml`: Configuration for the MCP Toolbox.
- `agent.py`: ADK Agent code.

## Prerequisites

1.  GCP Project: `skillful-signer-491109-r0`
2.  Terraform installed.
3.  `gcloud` CLI installed and authenticated.
4.  Root `.env` file configured with `GOOGLE_CLOUD_PROJECT`, `REGION`, and `DB_PASSWORD`.

## Setup Instructions

All commands should be run from the **project root directory**.

### 1. Provision Infrastructure

```bash
make infra-init
make infra-apply
```

After the infrastructure is applied, retrieve your database password:

```bash
cd python/agents/agent-adk-toolbox-cloudsql/infra && terraform output -raw db_password
```

Add this password to your root `.env` as `DB_PASSWORD`.

### 2. Seed the Database

Once the Cloud SQL instance is ready, seed it with the sample jobs data:

```bash
make seed-db
```

### 3. Run the MCP Toolbox

The MCP Toolbox acts as the bridge between your agent and the database:

```bash
make run-toolbox
```

### 4. Run the Agent

In a new terminal (with the toolbox still running):

```bash
make run-rag
```
