import os
import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from .agent import root_agent

# Use the experimental ADK utility to convert the agent to an A2A service
# This automatically handles discovery, RPC, and agent cards
app = to_a2a(
    agent=root_agent,
    host=os.environ.get("HOST", "localhost"),
    port=int(os.environ.get("PORT", 8001)),
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
