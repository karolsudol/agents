import mcp.server.fastmcp as fastmcp
import httpx
from typing import Dict, Any

# Initialize FastMCP server
mcp = fastmcp.FastMCP("Weather Service")

# City coordinates for some common cities
CITIES = {
    "london": {"lat": 51.5074, "lon": -0.1278},
    "new york": {"lat": 40.7128, "lon": -74.0060},
    "tokyo": {"lat": 35.6895, "lon": 139.6917},
    "paris": {"lat": 48.8566, "lon": 2.3522},
    "berlin": {"lat": 52.5200, "lon": 13.4050},
    "warsaw": {"lat": 52.2297, "lon": 21.0122},
}


@mcp.tool()
async def get_weather(city: str) -> str:
    """Retrieves real-time weather data from a REST API (Open-Meteo).

    Args:
        city (str): The name of the city (e.g., London, Warsaw, Tokyo).
    """
    city_lower = city.lower()
    if city_lower not in CITIES:
        return f"Error: City '{city}' not supported in this demo. Supported: {', '.join(CITIES.keys())}"

    coords = CITIES[city_lower]

    url = "https://api.open-meteo.com/v1/forecast"
    # Explicitly type the dictionary to satisfy Pyright/Pylance "partially unknown" checks
    params: Dict[str, Any] = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current_weather": "true",
        "timezone": "auto",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        return f"Error fetching weather: {response.status_code}"

    data = response.json()
    cw = data.get("current_weather", {})
    temp = cw.get("temperature")
    wind = cw.get("windspeed")

    return f"The real-time weather in {city.capitalize()} is {temp}°C with a wind speed of {wind} km/h."


if __name__ == "__main__":
    mcp.run()
