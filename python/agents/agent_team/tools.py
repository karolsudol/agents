from typing import Any, Optional, Dict, Union
from google.adk.tools.tool_context import ToolContext


def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet.
    """
    if name:
        return f"Hello, {name}!"
    return "Hello there!"


def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    return "Goodbye! Have a great day."


def get_weather(city: str, tool_context: ToolContext) -> Dict[str, Union[str, None]]:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").
    """
    # Key Concept: Reading from Session State
    preferred_unit = tool_context.state.get(
        "user_preference_temperature_unit", "Celsius"
    )

    city_normalized = city.lower().replace(" ", "")

    # Mock database
    mock_db: dict[str, dict[str, Any]] = {
        "newyork": {"temp_c": 25.0, "condition": "sunny"},
        "london": {"temp_c": 15.0, "condition": "cloudy"},
        "tokyo": {"temp_c": 18.0, "condition": "light rain"},
    }

    if city_normalized in mock_db:
        data = mock_db[city_normalized]
        temp_c: float = float(data["temp_c"])

        if str(preferred_unit) == "Fahrenheit":
            temp = (temp_c * 9 / 5) + 32
        else:
            temp = temp_c

        unit_str = "°F" if str(preferred_unit) == "Fahrenheit" else "°C"

        report = f"The weather in {city.capitalize()} is {data['condition']} with a temperature of {temp:.0f}{unit_str}."

        # Key Concept: Writing back to state
        tool_context.state["last_city_checked"] = city

        success_res: Dict[str, Union[str, None]] = {
            "status": "success",
            "report": report,
            "error_message": None,
        }
        return success_res

    error_res: Dict[str, Union[str, None]] = {
        "status": "error",
        "report": None,
        "error_message": f"Sorry, I don't have weather for '{city}'.",
    }
    return error_res
