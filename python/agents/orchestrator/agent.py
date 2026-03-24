# This is the standard entrypoint for the 'adk run' command.
# It simply exports the root agent of your team.
from .agents import team_orchestrator

# ADK looks for a variable named 'root_agent' by default.
root_agent = team_orchestrator
