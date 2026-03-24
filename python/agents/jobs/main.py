import os
import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from .agent import root_agent
from .plugins import JobsDomainSentinel

# Initialize Service-Side Governance
domain_sentinel = JobsDomainSentinel()

# Attach the sentinel to the agent's callbacks
# This ensures protection even when running as a standalone service
root_agent.before_model_callback = domain_sentinel.before_model_callback

# Convert the agent to an A2A service
app = to_a2a(
    agent=root_agent,
    host=os.environ.get("HOST", "localhost"),
    port=int(os.environ.get("PORT", 8001)),
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
