import datetime
import pytz
from google.adk.agents.llm_agent import Agent


def get_current_time(city: str) -> dict[str, str]:
    """Returns the current time in a specified city.
    Args:
        city: The name of the city (e.g., 'London', 'New York', 'Tokyo').
    """
    try:
        # Simple mapping for common cities, ideally use a geocoding API or more robust library
        city_to_tz = {
            "london": "Europe/London",
            "new york": "America/New_York",
            "tokyo": "Asia/Tokyo",
            "paris": "Europe/Paris",
            "berlin": "Europe/Berlin",
            "warsaw": "Europe/Warsaw",
        }
        
        timezone_str = city_to_tz.get(city.lower(), "UTC")
        timezone = pytz.timezone(timezone_str)
        now = datetime.datetime.now(timezone)
        return {
            "status": "success",
            "city": city,
            "timezone": timezone_str,
            "time": now.strftime("%I:%M %p"),
            "date": now.strftime("%Y-%m-%d")
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


root_agent = Agent(
    model="gemini-2.5-flash",
    name="single_tool_agent",
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)
