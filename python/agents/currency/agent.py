from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from ..constants import DEFAULT_MODEL
import os

# Define the path to the currency MCP server
# We use 'uv run' to ensure dependencies from pyproject.toml are used
CURRENCY_SERVER_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "mcp_servers", "currency", "server.py"
)

# Initialize the MCP Toolset using Stdio
currency_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=["run", "python", CURRENCY_SERVER_PATH],
        )
    )
)

root_agent = Agent(
    name="currency_agent",
    model=DEFAULT_MODEL,
    description="An agent specialized in currency conversion and financial exchange rates.",
    instruction="""You are a Currency Expert. You help users convert amounts between different currencies.
    - Use the 'convert_currency' tool to perform accurate conversions.
    - If a user asks for a currency you don't support, politely list the ones you do.
    - Be helpful, precise, and professional.""",
    tools=[currency_toolset],
)
