from google.adk.agents import Agent
from .tools import get_weather
from ..constants import DEFAULT_MODEL

root_agent = Agent(
    name="weather_agent",
    model=DEFAULT_MODEL,
    description="An agent specialized in weather reporting for global cities.",
    instruction="""You are a Weather Expert. You help users get real-time weather reports for cities.
    - Use the 'get_weather' tool to fetch data.
    - Always state the temperature and condition clearly.
    - Be helpful and precise.""",
    tools=[get_weather],
)
