from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from .agents import weather_agent_team

# Constant for the entire app
APP_NAME = "agent_team_app"

# Singleton session service
session_service = InMemorySessionService()


def create_request_runner():
    """Creates a FRESH runner for the current request using the shared session service."""
    return Runner(
        agent=weather_agent_team, app_name=APP_NAME, session_service=session_service
    )
