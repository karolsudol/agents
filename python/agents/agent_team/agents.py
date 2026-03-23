from google.adk.agents import Agent
from .tools import say_hello, say_goodbye, get_weather
from .callbacks import block_keyword_guardrail, block_paris_tool_guardrail

# Model Constant
MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash"

# Specialist 1: Greeting Agent
greeting_agent = Agent(
    name="greeting_agent",
    model=MODEL_GEMINI_2_5_FLASH,
    description="Handles simple greetings and hellos.",
    instruction="""You are the Greeting Agent. Your ONLY task is to provide a friendly greeting.
                   Use the 'say_hello' tool. If the user provides their name, pass it to the tool.""",
    tools=[say_hello],
)

# Specialist 2: Farewell Agent
farewell_agent = Agent(
    name="farewell_agent",
    model=MODEL_GEMINI_2_5_FLASH,
    description="Handles simple farewells and goodbyes.",
    instruction="""You are the Farewell Agent. Your ONLY task is to provide a polite goodbye.
                   Use the 'say_goodbye' tool when the user indicates they are leaving.""",
    tools=[say_goodbye],
)

# ROOT AGENT: The Coordinator
weather_agent_team = Agent(
    name="weather_agent_v2",
    model=MODEL_GEMINI_2_5_FLASH,
    description="The main coordinator agent for weather and general conversation.",
    instruction="""You are the main Weather Agent. Your primary responsibility is weather.
                   - If user asks for weather: Use the 'get_weather' tool yourself.
                   - If user says Hi/Hello: Delegate to 'greeting_agent'.
                   - If user says Bye: Delegate to 'farewell_agent'.
                   - For anything else, be helpful or say you can only handle weather and greetings.""",
    tools=[get_weather],
    sub_agents=[greeting_agent, farewell_agent],
    # Add Guardrails!
    before_model_callback=block_keyword_guardrail,  # Intercepts input
    before_tool_callback=block_paris_tool_guardrail,  # Intercepts tool calls
)
