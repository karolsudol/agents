from google.adk.agents import Agent
from ..agent_toolbox_mcp.agent import root_agent as jobs_agent
from ..agent_spanner_mcp.agent import root_agent as spanner_graph_agent
from ..agent_currency.agent import root_agent as currency_agent
from .tools import say_hello, say_goodbye, get_weather

# Model Constant
MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash"

# ROOT AGENT: The Master Orchestrator (A2A)
team_orchestrator = Agent(
    name="team_orchestrator",
    model=MODEL_GEMINI_2_5_FLASH,
    description="The central entry point for all agent services. Orchestrates specialized agents for jobs, finance, and currency.",
    instruction="""You are the Master Orchestrator of a team of specialized AI agents.
Your goal is to delegate user requests to the most appropriate specialist:

- For job searches, tech stack inquiries, or recruitment: Delegate to 'jobs_agent'.
- For financial fraud detection, account transfers, or Spanner graph analysis: Delegate to 'spanner_graph_agent'.
- For currency conversion and exchange rates: Delegate to 'currency_agent'.
- For greetings or small talk: Use 'say_hello' or 'say_goodbye' tools.
- For current weather info: Use 'get_weather' tool.

If a request spans multiple domains (e.g., "Find me a job in London and convert the salary from USD to GBP"),
coordinate between the agents sequentially.

Be a professional and efficient coordinator. Always provide a final synthesis of the specialists' findings to the user.""",
    tools=[say_hello, say_goodbye, get_weather],
    sub_agents=[jobs_agent, spanner_graph_agent, currency_agent],
)

# Alias for compatibility with run-agent
root_agent = team_orchestrator
