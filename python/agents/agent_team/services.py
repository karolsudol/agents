from typing import Any, Optional
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from .agents import weather_agent_team

# Key Concept: The SessionService stores the conversation context.
session_service = InMemorySessionService()


# Key Concept: The Runner orchestrates the Agent Team loop.
def get_runner():
    """Returns a configured Runner for our agent team."""
    return Runner(
        agent=weather_agent_team,
        app_name="agent_team_app",
        session_service=session_service,
    )


async def initialize_session(
    user_id: str, session_id: str, initial_state: Optional[dict[str, Any]] = None
) -> Any:
    """Creates a session with initial state (e.g., user preferences)."""
    return await session_service.create_session(
        app_name="agent_team_app",
        user_id=user_id,
        session_id=session_id,
        state=initial_state or {"user_preference_temperature_unit": "Celsius"},
    )
