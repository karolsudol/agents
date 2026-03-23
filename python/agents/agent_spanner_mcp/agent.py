from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
import google.auth
import google.auth.transport.requests

# Spanner MCP Configuration
SPANNER_MCP_URL = "https://spanner.googleapis.com/mcp"


def get_google_auth_headers():
    credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/spanner.admin",
            "https://www.googleapis.com/auth/spanner.data",
            "https://www.googleapis.com/auth/cloud-platform",
        ]
    )
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)
    return {"Authorization": f"Bearer {credentials.token}"}


# Initialize the Spanner MCP Toolset
# Note: SseConnectionParams expects headers for the initial connection
spanner_toolset = McpToolset(
    connection_params=SseConnectionParams(
        url=SPANNER_MCP_URL, headers=get_google_auth_headers()
    )
)

root_agent = Agent(
    name="spanner_graph_agent",
    model="gemini-1.5-flash",
    description="An agent specialized in financial fraud detection using Spanner Property Graphs.",
    instruction="""You are a Fraud Detection Expert. You have access to a Cloud Spanner database with a financial property graph (FinGraph).
    Your task is to:
    - Help users explore account transfers and relationships.
    - Identify potential fraud patterns like circular transfers (e.g., A -> B -> C -> A).
    - Provide insights into blocked accounts and their connections.

    Use the tools provided by the Spanner MCP server to query the graph.
    When a user asks about transfers or owners, use the appropriate Spanner Graph tools.
    Be analytical, precise, and helpful.""",
    tools=[spanner_toolset],
)
