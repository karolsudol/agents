import datetime
import pytz
from google.adk.agents.llm_agent import Agent
from ..constants import DEFAULT_MODEL


def get_weather(city: str) -> dict[str, str]:
    """Retrieves the current weather report for a specified city.
    Args:
        city: The name of the city for which to retrieve the weather report.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": "The weather in New York is sunny with a temperature of 25°C (77°F).",
        }
    return {
        "status": "error",
        "error_message": f"Weather information for '{city}' is not available.",
    }


def get_current_time(city: str) -> dict[str, str]:
    """Returns the current time in a specified city.
    Args:
        city: The name of the city (e.g., 'London', 'New York', 'Tokyo').
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
        timezone_str = city_to_tz.get(city.lower(), "UTC")
        timezone = pytz.timezone(timezone_str)
        now = datetime.datetime.now(timezone)
        return {
            "status": "success",
            "city": city,
            "time": now.strftime("%I:%M %p"),
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


def describe_audio(audio_info: str) -> dict[str, str]:
    """Provides a detailed description or analysis of an audio file's content.
    Args:
        audio_info: Information or path to the audio to be analyzed.
    """
    return {
        "status": "success",
        "analysis": f"Successfully analyzed audio: {audio_info}",
        "summary": "Audio contains spoken dialogue with minimal background noise.",
    }


root_agent = Agent(
    model=DEFAULT_MODEL,
    name="multimodal_multi_tool_agent",
    description="A powerful multimodal agent that can analyze audio, tell the time, and check the weather.",
    instruction=(
        "You are an expert multimodal assistant. You can process text instructions, "
        "analyze audio content with 'describe_audio', and answer questions about "
        "the time or weather using the provided tools."
    ),
    tools=[describe_audio, get_weather, get_current_time],
)
