# 🏢 Corporate AI Hub (Master Orchestrator)

This project demonstrates a production-grade multi-agent team following the **Agentverse Architect** model. It features delegation, persistent long-term memory, looping protocols, and advanced governance.

## 🏗️ Structure
- **`agents.py`**: Corporate Hub Orchestrator + Sentinel Guardrail.
- **`plugins.py`**: Governance Plugins (e.g., CoolDown/Governor).
- **`services.py`**: Persistent Session Management (SQLite).
- **`main.py`**: FastAPI entrypoint with `/chat` endpoint.

## 🚀 Key Features
1. **Long-Term Memory**: Uses SQLite to remember session state across restarts.
2. **Looping Protocol**: The `risk_analyst` iteratively audits data until approved.
3. **Parallel Execution**: Orchestrator can trigger simultaneous compliance and risk scans.
4. **Governance**:
   - **Sentinel**: Blocks forbidden terms (e.g., "internal secrets").
   - **Governor**: Enforces a 60-second cooldown per session.

## 🚀 How to Run

### Option 1: CLI Mode (adk run)
To run the agent in the terminal (standard ADK loop):
```bash
make run-a2a
```

### Option 2: REST API Mode (FastAPI)
To start the FastAPI server on port 8000:
```bash
make run-team-api
```

To test the running API:
```bash
make test-team-api
```

#### Test with cURL
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "user_id": "manager_1",
           "session_id": "audit_sess_001",
           "message": "Run a full risk audit on the Spanner finance graph.",
           "temp_unit": "Celsius"
         }'
```
