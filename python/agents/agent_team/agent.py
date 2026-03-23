# This is the standard entrypoint for the 'adk run' command.
# It simply exports the root agent of your team.
from .agents import weather_agent_team

# ADK looks for a variable named 'agent' or 'root_agent' by default.
agent = weather_agent_team
