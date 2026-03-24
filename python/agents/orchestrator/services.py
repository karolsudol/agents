from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from .agents import team_orchestrator

# Constant for the entire app
APP_NAME = "agent_team_app"

# Singleton session service
session_service = InMemorySessionService()


def create_request_runner():
    """Creates a FRESH runner for the current request using the shared session service."""
    return Runner(
        agent=team_orchestrator, app_name=APP_NAME, session_service=session_service
    )
