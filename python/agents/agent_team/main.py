from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google.genai import types

# Import our agent team components
from .services import get_runner, initialize_session, session_service

# Load environment variables (API Key)
load_dotenv()

app = FastAPI(title="Agent Team API")


# Request Model
class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str
    temp_unit: Optional[str] = "Celsius"


@app.post("/chat")
async def chat(request: ChatRequest) -> dict[str, str]:
    """Sends a message to the agent team and returns the final response."""
    app_name = "agent_team_app"

    # 1. Ensure the session exists
    session = await session_service.get_session(
        app_name=app_name, user_id=request.user_id, session_id=request.session_id
    )

    if not session:
        print(f"--- Session {request.session_id} not found. Initializing... ---")
        await initialize_session(
            user_id=request.user_id,
            session_id=request.session_id,
            initial_state={"user_preference_temperature_unit": request.temp_unit},
        )
    else:
        print(f"--- Using existing session {request.session_id} ---")

    # 2. Get the runner and prepare the message
    runner = get_runner()
    content = types.Content(role="user", parts=[types.Part(text=request.message)])

    final_response = "Agent did not produce a final response."

    # 3. Run the agent team and wait for events
    try:
        async for event in runner.run_async(
            user_id=request.user_id, session_id=request.session_id, new_message=content
        ):
            # We look for the final response from the agent
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = (
                        event.content.parts[0].text
                        or "Agent produced an empty response."
                    )
                elif event.actions and event.actions.escalate:
                    final_response = f"Agent escalated: {event.error_message or 'No error message provided.'}"
                break

        return {"response": final_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
