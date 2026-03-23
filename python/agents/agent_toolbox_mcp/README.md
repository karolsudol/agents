# Agentic RAG with MCP Toolbox for Databases

This agent uses the **MCP Toolbox for Databases** to bridge a Gemini-powered agent with **Cloud SQL (PostgreSQL)**.

## Project Structure (Moved to Root)

- `/infra/`: Terraform configuration for GCP resources.
- `/sql/seed.sql`: SQL script to initialize the database and seed it with jobs.
- `/tools.yaml`: Configuration for the MCP Toolbox.
- `agent.py`: ADK Agent code.

## Prerequisites

1.  **GCP Project**: A Google Cloud Project with billing enabled.
2.  **gcloud CLI**: Installed and authenticated.
    - **Install**: `curl -sSL https://sdk.cloud.google.com | bash`
    - **Init**: `gcloud init`
    - **Authenticate**: `gcloud auth application-default login`
3.  **Environment Variables**: A root `.env` file (see below).

## Setup Instructions

All commands MUST be run from the **project root directory**.

### 1. Initialize Environment
This will download the necessary binaries (`terraform`, `toolbox`, `cloud-sql-proxy`) and sync Python dependencies.

```bash
make setup
```

### 2. Configure Environment Variables
Create or update your root `.env` file with your project details:

```text
GOOGLE_CLOUD_PROJECT="<YOUR_PROJECT_ID>"
REGION="europe-west1"
DB_PASSWORD=""
TOOLBOX_URL="http://127.0.0.1:5000"
```

### 3. Provision Infrastructure
Deploy Cloud SQL, enable APIs, and set up IAM permissions.

```bash
make infra-init
make infra-apply
```

After the infrastructure is applied, retrieve your generated database password and add it to your `.env`:

```bash
./terraform -chdir=infra output -raw db_password
```

### 4. Seed the Database
Populate the Cloud SQL instance with sample job listings and generate vector embeddings.

```bash
make seed-db
```

### 5. Run the MCP Toolbox
The toolbox acts as the bridge between your agent and the database. Keep this running in a separate terminal.

```bash
make run-toolbox
```

### 6. Run the Agent
In a new terminal window, run the ADK Agent:

```bash
make run-rag
```
