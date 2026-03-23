# This is the standard entrypoint for the 'adk run' command.
# It simply exports the root agent of your team.
from .agents import weather_agent_team

# ADK looks for a variable named 'root_agent' by default.
root_agent = weather_agent_team
