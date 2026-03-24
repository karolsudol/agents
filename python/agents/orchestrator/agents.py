import os
from typing import List
from google.adk.agents import Agent, BaseAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# Local Imports
from ..finance.agent import root_agent as finance_director
from ..weather.agent import root_agent as logistics_agent
from .tools import say_hello, say_goodbye
from .plugins import CoolDownPlugin
from ..constants import DEFAULT_MODEL

# Determine Execution Path (Local vs Remote A2A)
USE_REMOTE_A2A = os.environ.get("USE_REMOTE_A2A", "false").lower() == "true"
JOBS_SERVICE_URL = os.environ.get("JOBS_SERVICE_URL", "http://localhost:8001")

# Specialized Agents container
# We use list[BaseAgent] to avoid type invariance issues with pyright
sub_agents: List[BaseAgent] = [finance_director, logistics_agent]

if USE_REMOTE_A2A:
    print(f"[A2A] Initializing Remote A2A Connection for Jobs at {JOBS_SERVICE_URL}")
    # Using the RemoteA2aAgent Pattern (Enterprise Pattern)
    # The agent_card can be a URL to the remote service's metadata
    jobs_remote = RemoteA2aAgent(
        name="hr_recruitment_service", agent_card=JOBS_SERVICE_URL
    )
    sub_agents.append(jobs_remote)
else:
    print("[A2A] Running in Local Monolith Mode")
    from ..jobs.agent import root_agent as hr_director

    sub_agents.append(hr_director)

# Governance
cooldown_governor = CoolDownPlugin(cooldown_seconds=60)

# ROOT AGENT: The Corporate Hub (Master Orchestrator)
team_orchestrator = Agent(
    name="corporate_hub_orchestrator",
    model=DEFAULT_MODEL,
    description="The central intelligence for all corporate domains.",
    instruction=f"""You are the Master Orchestrator.
    Execution Mode: {"Remote A2A" if USE_REMOTE_A2A else "Local Monolith"}.

    Delegate to specialized departments:
    - HR/Recruitment: Use 'hr_recruitment_service'.
    - Finance/Risk: Delegate to 'finance_director'.
    - Logistics: Delegate to 'logistics_agent'.

    Coordinate across domains to fulfill corporate requests.""",
    tools=[say_hello, say_goodbye],
    sub_agents=sub_agents,
    before_agent_callback=cooldown_governor.before_agent_callback,
)

root_agent = team_orchestrator
