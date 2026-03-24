from google.adk.agents import Agent
from ..jobs.agent import root_agent as jobs_agent
from ..spanner.agent import root_agent as spanner_graph_agent
from ..currency.agent import root_agent as currency_agent
from ..weather.agent import root_agent as weather_agent
from .tools import say_hello, say_goodbye
from ..constants import DEFAULT_MODEL

# ROOT AGENT: The Master Orchestrator (A2A)
team_orchestrator = Agent(
    name="team_orchestrator",
    model=DEFAULT_MODEL,
    description="The central entry point for all agent services. Orchestrates specialized agents for jobs, finance, currency, and weather.",
    instruction="""You are the Master Orchestrator of a team of specialized AI agents.
Your goal is to delegate user requests to the most appropriate specialist:

- For job searches, tech stack inquiries, or recruitment: Delegate to 'jobs_agent'.
- For financial fraud detection, account transfers, or Spanner graph analysis: Delegate to 'spanner_graph_agent'.
- For currency conversion and exchange rates: Delegate to 'currency_agent'.
- For current weather info: Delegate to 'weather_agent'.
- For greetings or small talk: Use 'say_hello' or 'say_goodbye' tools.

If a request spans multiple domains (e.g., "Find me a job in London and convert the salary from USD to GBP"),
coordinate between the agents sequentially.

Be a professional and efficient coordinator. Always provide a final synthesis of the specialists' findings to the user.""",
    tools=[say_hello, say_goodbye],
    sub_agents=[jobs_agent, spanner_graph_agent, currency_agent, weather_agent],
)

# Alias for compatibility with run-agent
root_agent = team_orchestrator
