from google.adk.agents import Agent
from agents.currency.agent import root_agent as treasury_agent
from agents.spanner.agent import root_agent as spanner_agent
from agents.constants import DEFAULT_MODEL

# specialist 1: The Data Gatherer (Used by Risk)
data_gatherer = Agent(
    name="data_gatherer",
    model=DEFAULT_MODEL,
    description="Extracts raw financial figures.",
    instruction="Focus on accuracy. Extract transfer data from Spanner.",
)

# Specialist 2: The Critical Reviewer (Used by Risk)
critical_reviewer = Agent(
    name="critical_reviewer",
    model=DEFAULT_MODEL,
    description="Audits financial reports.",
    instruction="If data is missing, state 'REJECT'. If valid, state 'APPROVED'.",
)

# LOOPING AGENT: Iterative Risk Analyst
risk_analyst = Agent(
    name="risk_analyst",
    model=DEFAULT_MODEL,
    description="Performs iterative risk assessments.",
    instruction="""LOOPING PROTOCOL:
    1. SUMMON 'data_gatherer'.
    2. SUMMON 'critical_reviewer' to audit.
    3. IF 'REJECT', RE-SUMMON 'data_gatherer' with feedback.
    4. LOOP until 'APPROVED'.""",
    sub_agents=[data_gatherer, critical_reviewer],
)

# DEPARTMENT HEAD: Finance Director (Hierarchical Routing)
finance_director = Agent(
    name="finance_director",
    model=DEFAULT_MODEL,
    description="Head of Finance. Manages Treasury and Risk.",
    instruction="""You are the Finance Director.
    - For currency/FX: Delegate to 'treasury_agent'.
    - For risk/fraud/audit: Delegate to 'risk_analyst'.
    - For Spanner graph queries: Delegate to 'spanner_agent'.""",
    sub_agents=[treasury_agent, risk_analyst, spanner_agent],
)

# Export the Director as the root of this domain
root_agent = finance_director
