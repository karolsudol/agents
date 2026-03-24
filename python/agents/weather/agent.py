from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import os
from agents.constants import DEFAULT_MODEL

# Define the path to the weather MCP server
WEATHER_SERVER_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "mcp_servers", "weather", "server.py"
)

# Initialize the MCP Toolset using Stdio
weather_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=["run", "python", WEATHER_SERVER_PATH],
        )
    )
)

root_agent = Agent(
    name="weather_agent",
    model=DEFAULT_MODEL,
    description="An agent specialized in fetching real-time weather data.",
    instruction="""You are a Weather Expert. You fetch REAL-TIME weather data.
    - Use the 'get_weather' tool provided by the MCP server.
    - Always provide the current temperature and wind conditions.
    - Be professional and analytical.""",
    tools=[weather_toolset],
)
