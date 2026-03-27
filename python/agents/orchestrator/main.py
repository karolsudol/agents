import json
from typing import Any, Dict
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google.genai import types

# Import modular components
from .services import session_service, create_request_runner, APP_NAME

# Load environment variables
load_dotenv()

app = FastAPI(title="AG-UI Compliant Agent API")


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str
    temp_unit: str = "Celsius"


@app.get("/")
async def root():
    return {"status": "alive", "message": "AG-UI & UCP Hub is running."}


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest, raw_request: Request):
    """
    AG-UI (Agent-User Interaction) compliant SSE endpoint.
    Translates ADK events into standardized AG-UI event types.
    """

    async def event_generator():
        # 1. Initialize Session
        try:
            await session_service.create_session(
                app_name=APP_NAME,
                user_id=request.user_id,
                session_id=request.session_id,
                state={"user_preference_temperature_unit": request.temp_unit},
            )
        except Exception:
            pass

        runner = create_request_runner()
        content = types.Content(role="user", parts=[types.Part(text=request.message)])

        # 2. Stream Events via AG-UI Protocol
        try:
            async for event in runner.run_async(
                user_id=request.user_id,
                session_id=request.session_id,
                new_message=content,
            ):
                ag_ui_event: Dict[str, Any] = {"type": "UNKNOWN", "data": {}}

                # Check for Tool Calls
                function_calls = event.get_function_calls()

                if function_calls:
                    fc = function_calls[0]
                    ag_ui_event = {
                        "type": "TOOL_CALL_START",
                        "data": {"tool_name": fc.name, "args": fc.args},
                    }
                # Check for Text Content
                elif event.content and event.content.parts:
                    text_parts = [p.text for p in event.content.parts if p.text]
                    if text_parts:
                        text_content = "".join(text_parts)

                        if event.is_final_response():
                            ag_ui_event = {
                                "type": "MESSAGE_COMPLETE",
                                "data": {"final_text": text_content},
                            }
                        else:
                            ag_ui_event = {
                                "type": "TEXT_MESSAGE_CONTENT",
                                "data": {"text": text_content},
                            }
                elif event.is_final_response():
                    ag_ui_event = {
                        "type": "MESSAGE_COMPLETE",
                        "data": {"final_text": ""},
                    }

                if ag_ui_event["type"] != "UNKNOWN":
                    yield {
                        "event": ag_ui_event["type"],
                        "data": json.dumps(ag_ui_event["data"]),
                    }

        except Exception as e:
            yield {"event": "ERROR", "data": json.dumps({"detail": str(e)})}

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
