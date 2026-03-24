from typing import Any, Optional
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types


def block_keyword_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Intercepts user input and blocks the LLM if forbidden words are found."""

    # We scan the last message from the user
    last_user_msg = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts:
                last_user_msg = content.parts[0].text or ""
                break

    if "BLOCK" in last_user_msg.upper():
        print("--- Guardrail: Block keyword detected! ---")
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="I am sorry, but I cannot process requests containing blocked keywords."
                    )
                ],
            )
        )
    return None  # Return None to let the LLM call proceed


def block_paris_tool_guardrail(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> Optional[dict[str, Any]]:
    """Blocks specific tool calls based on arguments."""

    # Let's block 'Paris' for demonstration
    if tool.name == "get_weather":
        city = str(args.get("city", "")).lower()
        if "paris" in city:
            print("--- Guardrail: Blocking weather for Paris! ---")
            return {
                "status": "error",
                "error_message": "Policy Restriction: Weather for Paris is currently disabled.",
            }
    return None  # Return None to allow the tool to run
