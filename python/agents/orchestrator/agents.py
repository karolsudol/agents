from google.adk.agents import Agent
from ..jobs.agent import root_agent as hr_director
from ..finance.agent import root_agent as finance_director
from ..weather.agent import root_agent as logistics_agent
from .tools import say_hello, say_goodbye
from .plugins import CoolDownPlugin
from ..constants import DEFAULT_MODEL

# Governance & Safety
cooldown_governor = CoolDownPlugin(cooldown_seconds=60)

# Specialists for Parallel Demo
compliance_scanner = Agent(
    name="compliance_scanner", model=DEFAULT_MODEL, description="Scans policies."
)
legal_reviewer = Agent(
    name="legal_reviewer", model=DEFAULT_MODEL, description="Reviews legal risks."
)

# ROOT AGENT: The Corporate Hub (Master Orchestrator)
team_orchestrator = Agent(
    name="corporate_hub_orchestrator",
    model=DEFAULT_MODEL,
    description="The central intelligence for all corporate domains.",
    instruction="""You are the Master Orchestrator. Follow these capability protocols:

    1. HIERARCHICAL ROUTING:
       - Delegate to 'finance_director' for ALL financial, FX, or risk tasks.
       - Delegate to 'hr_director' for recruitment/jobs (Agentic RAG).
       - Delegate to 'logistics_agent' for weather/external conditions.

    2. PARALLEL EXECUTION:
       - For corporate audits, SUMMON 'compliance_scanner' and 'legal_reviewer' SIMULTANEOUSLY.

    3. MEMORY:
       - SHORT-TERM: Use session state to track the user's current intent.
       - LONG-TERM: Reference the persistent SQLite store for past interactions.

    Synthesize all specialist results into a professional corporate briefing.""",
    tools=[say_hello, say_goodbye],
    sub_agents=[
        finance_director,
        hr_director,
        logistics_agent,
        compliance_scanner,
        legal_reviewer,
    ],
    before_agent_callback=cooldown_governor.before_agent_callback,
)

root_agent = team_orchestrator
