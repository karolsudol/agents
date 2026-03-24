import os
from typing import List
from google.adk.agents import Agent, BaseAgent

# Use Absolute Imports to prevent "beyond top-level package" errors
from agents.finance.agent import root_agent as finance_director
from agents.weather.agent import root_agent as logistics_agent
from agents.orchestrator.tools import say_hello, say_goodbye
from agents.orchestrator.plugins import CoolDownPlugin
from agents.constants import DEFAULT_MODEL

# Determine Execution Path (Local vs Remote A2A)
USE_REMOTE_A2A = os.environ.get("USE_REMOTE_A2A", "false").lower() == "true"
JOBS_SERVICE_URL = os.environ.get("JOBS_SERVICE_URL", "http://localhost:8001")

# Specialized Agents container
sub_agents: List[BaseAgent] = [finance_director, logistics_agent]

if USE_REMOTE_A2A:
    print(f"[A2A] Initializing Remote A2A Connection for Jobs at {JOBS_SERVICE_URL}")
    # Lazy import to avoid ModuleNotFoundError
    from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

    jobs_remote = RemoteA2aAgent(
        name="hr_recruitment_service", agent_card=JOBS_SERVICE_URL
    )
    sub_agents.append(jobs_remote)
else:
    print("[A2A] Running in Local Monolith Mode")
    from agents.jobs.agent import root_agent as hr_director

    sub_agents.append(hr_director)

# Governance
cooldown_governor = CoolDownPlugin(cooldown_seconds=60)

# Specialists for Parallel Demo
compliance_scanner = Agent(
    name="compliance_scanner", model=DEFAULT_MODEL, description="Scans policies."
)
legal_reviewer = Agent(
    name="legal_reviewer", model=DEFAULT_MODEL, description="Reviews legal risks."
)
sub_agents.extend([compliance_scanner, legal_reviewer])

# ROOT AGENT: The Corporate Hub (Master Orchestrator)
team_orchestrator = Agent(
    name="corporate_hub_orchestrator",
    model=DEFAULT_MODEL,
    description="The central intelligence for all corporate domains.",
    instruction=f"""You are the Master Orchestrator.
    Execution Mode: {"Remote A2A" if USE_REMOTE_A2A else "Local Monolith"}.

    Follow these capability protocols:

    1. HIERARCHICAL ROUTING:
       - Delegate to 'finance_director' for ALL financial, FX, or risk tasks.
       - Delegate to {"hr_recruitment_service" if USE_REMOTE_A2A else "hr_director"} for recruitment/jobs.
       - Delegate to 'logistics_agent' for weather/external conditions.

    2. PARALLEL EXECUTION:
       - For corporate audits, SUMMON 'compliance_scanner' and 'legal_reviewer' SIMULTANEOUSLY.

    3. MEMORY:
       - SHORT-TERM: Use session state to track context.
       - LONG-TERM: Reference the persistent store for past interactions.

    Synthesize all results into a professional corporate briefing.""",
    tools=[say_hello, say_goodbye],
    sub_agents=sub_agents,
    before_agent_callback=cooldown_governor.before_agent_callback,
)

root_agent = team_orchestrator
