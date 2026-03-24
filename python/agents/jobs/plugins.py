from typing import Optional
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from google.adk.models.llm_request import LlmRequest


class JobsDomainSentinel:
    """
    Service-Side Governance: This plugin lives inside the Jobs A2A Service.
    It provides domain-specific protection that applies even if the agent is called directly.
    """

    def before_model_callback(
        self, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> Optional[LlmResponse]:
        """
        Intercepts requests at the service boundary.
        """
        print(
            f"[Service-Governance] Jobs boundary check for session: {callback_context.session.id}"
        )

        # Example: Block requests that try to access restricted executive salaries
        last_user_msg = ""
        if llm_request.contents:
            for content in reversed(llm_request.contents):
                if content.role == "user" and content.parts:
                    last_user_msg = content.parts[0].text or ""
                    break

        if (
            "ceo" in last_user_msg.lower()
            or "salary" in last_user_msg.lower()
            and "executive" in last_user_msg.lower()
        ):
            print(
                "[Service-Governance] BLOCKED: Unauthorized access to executive data."
            )
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            text="Error: Domain Policy Violation. You do not have clearance to access executive salary data."
                        )
                    ],
                )
            )

        return None
