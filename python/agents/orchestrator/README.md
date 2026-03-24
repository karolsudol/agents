# 🤖 Weather Agent Team (Research Project)

This project demonstrates a multi-agent team with delegation, state management, and safety guardrails, all exposed via a FastAPI REST interface.

## 🏗️ Structure
- **`agents.py`**: Root agent (Weather) + Sub-agents (Greeting, Farewell).
- **`tools.py`**: State-aware weather lookup tool.
- **`callbacks.py`**: Input/Tool guardrails (blocks "BLOCK" keyword and "Paris" weather).
- **`main.py`**: FastAPI entrypoint with `/chat` endpoint.

## 🚀 How to Run

### Option 1: CLI Mode (adk run)
To run the agent in the terminal (standard ADK loop):
```bash
make run-agent NAME=agent_team
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
           "user_id": "karol_1",
           "session_id": "sess_001",
           "message": "Hello, my name is Karol! What is the weather in London?",
           "temp_unit": "Celsius"
         }'
```

## 🛡️ Guardrails to Test
1. **Keyword Guardrail**: Try sending a message with the word "BLOCK".
2. **Tool Guardrail**: Try asking for the weather in "Paris".
3. **Delegation**: Try saying "Hi" or "Bye" - the root agent will delegate to the specialists!
