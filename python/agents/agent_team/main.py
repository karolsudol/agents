from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google.genai import types

# Import our modular components
from .services import session_service, create_request_runner, APP_NAME

# Load API Key
load_dotenv()

app = FastAPI(title="Agent Team API")


@app.get("/")
async def root():
    return {"status": "alive", "message": "Agent Team API is running."}


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str
    temp_unit: str = "Celsius"


@app.post("/chat")
async def chat(request: ChatRequest):
    """Sends a message to the agent team using a fresh runner per request."""

    # 1. MANDATORY: Create/Get session in the same scope as the runner
    try:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=request.user_id,
            session_id=request.session_id,
            state={"user_preference_temperature_unit": request.temp_unit},
        )
        print(f"--- [API] Session {request.session_id} created ---")
    except Exception:
        # Session already exists, which is expected on subsequent calls
        pass

    # 2. Create a fresh runner for this request
    runner = create_request_runner()

    content = types.Content(role="user", parts=[types.Part(text=request.message)])
    final_response = "No response from agent."

    # 3. Execute the run
    try:
        async for event in runner.run_async(
            user_id=request.user_id, session_id=request.session_id, new_message=content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text or "Empty response."
                break

        return {"response": final_response}

    except Exception as e:
        print(f"--- [API] Runner Error: {e} ---")
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
