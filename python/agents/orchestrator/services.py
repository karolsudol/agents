from google.adk.sessions.sqlite_session_service import SqliteSessionService
from google.adk.runners import Runner
from .agents import team_orchestrator

# Configuration
APP_NAME = "corporate_hub"
DB_PATH = "sessions.db"

# Use built-in SqliteSessionService for local persistence (Long-Term Memory)
session_service = SqliteSessionService(db_path=DB_PATH)


def create_request_runner():
    """Creates a FRESH runner using the persistent SQLite session service."""
    return Runner(
        agent=team_orchestrator, app_name=APP_NAME, session_service=session_service
    )
