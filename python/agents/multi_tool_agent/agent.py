import datetime
import pytz
from google.adk.agents.llm_agent import Agent

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    try:
        city_to_tz = {
            "london": "Europe/London",
            "new york": "America/New_York",
            "tokyo": "Asia/Tokyo",
            "paris": "Europe/Paris",
            "berlin": "Europe/Berlin",
            "warsaw": "Europe/Warsaw",
        }
        
        timezone_str = city_to_tz.get(city.lower())
        if not timezone_str:
             return {
                "status": "error",
                "error_message": (
                    f"Sorry, I don't have timezone information for {city}."
                ),
            }

        tz = pytz.timezone(timezone_str)
        now = datetime.datetime.now(tz)
        report = (
            f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
        )
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


root_agent = Agent(
    model="gemini-2.5-flash",
    name="weather_time_agent",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)
