from typing import Optional
from google.adk.agents import Agent
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from ..jobs.agent import root_agent as jobs_agent
from ..spanner.agent import root_agent as spanner_graph_agent
from ..currency.agent import root_agent as currency_agent
from ..weather.agent import root_agent as weather_agent
from ..finance.agent import root_agent as risk_analyst
from .tools import say_hello, say_goodbye
from .plugins import CoolDownPlugin
from ..constants import DEFAULT_MODEL

# Governance & Safety Instances
cooldown_governor = CoolDownPlugin(cooldown_seconds=60)


def sentinel_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    The 'Sentinel' (Safety Guardrail).
    Checks for high-risk terms before any model execution.
    """
    forbidden_keywords = ["internal secret", "admin override", "unrestricted access"]

    last_user_msg = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts:
                last_user_msg = content.parts[0].text or ""
                break

    query_lower = last_user_msg.lower()

    for word in forbidden_keywords:
        if word in query_lower:
            print(f"[Safety] Sentinel BLOCKED query: '{word}'")
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            text=f"Corporate Security Alert: Discussion of '{word}' is restricted to authorized personnel only."
                        )
                    ],
                )
            )

    return None


# Specialist: Parallel Compliance Engine
compliance_agent = Agent(
    name="compliance_agent",
    model=DEFAULT_MODEL,
    description="Checks corporate policies in parallel.",
    instruction="""Verify if the request complies with corporate expense and recruitment policies.""",
)

# ROOT AGENT: The Corporate Hub Orchestrator
team_orchestrator = Agent(
    name="corporate_hub_orchestrator",
    model=DEFAULT_MODEL,
    description="The central intelligence for Corporate Operations (Finance, HR, Logistics).",
    instruction="""You are the Corporate Hub Orchestrator.
    Delegate to specialized departments:
    - HR/Recruitment: 'jobs_agent' (Agentic RAG)
    - Financial Fraud: 'spanner_graph_agent'
    - Treasury/FX: 'currency_agent'
    - Logistics/Weather: 'weather_agent'
    - Audit/Risk: 'risk_analyst' (Looping Protocol)
    - Compliance: 'compliance_agent' (Parallel Execution)

    For complex audits, SUMMON 'risk_analyst' and 'compliance_agent' PARALLELY to ensure both risk and compliance are handled simultaneously.""",
    tools=[say_hello, say_goodbye],
    sub_agents=[
        jobs_agent,
        spanner_graph_agent,
        currency_agent,
        weather_agent,
        risk_analyst,
        compliance_agent,
    ],
    before_model_callback=sentinel_guardrail,
    before_agent_callback=cooldown_governor.before_agent_callback,
)

# Alias for compatibility
root_agent = team_orchestrator
