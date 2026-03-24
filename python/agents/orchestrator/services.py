import os
from google.adk.sessions.sqlite_session_service import SqliteSessionService
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.runners import Runner
from .agents import team_orchestrator

# Configuration
APP_NAME = "corporate_hub"
DB_PATH = "sessions.db"

# DUAL MEMORY PATHS
# Set PERSISTENT_MEMORY=false to use Ephemeral (Short-Term Only) mode
USE_PERSISTENT_MEMORY = os.environ.get("PERSISTENT_MEMORY", "true").lower() == "true"

if USE_PERSISTENT_MEMORY:
    print(f"[Memory] Initializing Long-Term Persistent Storage at {DB_PATH}")
    session_service = SqliteSessionService(db_path=DB_PATH)
else:
    print("[Memory] Initializing Ephemeral Short-Term Storage (InMemory)")
    session_service = InMemorySessionService()


def create_request_runner():
    """Creates a FRESH runner using the selected memory service."""
    return Runner(
        agent=team_orchestrator, app_name=APP_NAME, session_service=session_service
    )
