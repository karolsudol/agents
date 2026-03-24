# agent.py
import os
from google.adk.agents import Agent
from google.adk.tools.toolbox_toolset import ToolboxToolset
from constants import DEFAULT_MODEL

# Toolbox URL should point to the MCP Toolbox server
TOOLBOX_URL = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
toolbox = ToolboxToolset(TOOLBOX_URL)

root_agent = Agent(
    name="jobs_agent",
    model=DEFAULT_MODEL,
    description="A specialist in tech job recruitment using Agentic RAG.",
    instruction="""You are a Tech Recruitment Specialist. You MUST follow this DOMAIN PROTOCOL for every request:

1. ANALYZE: First, understand the candidate's core stack and work style.
2. RETRIEVE: Use 'search-jobs-by-description' for a semantic search (RAG) to find matches beyond just titles.
3. VERIFY: Check the 'openings' count. If a job has 0 openings, you MUST find an alternative.
4. SYNTHESIZE: Provide a concise summary of WHY these jobs fit the candidate's specific profile.

When in doubt, prioritize the 'search-jobs-by-description' tool as it is powered by Vertex AI embeddings.
Always be encouraging, data-driven, and brief.""",
    tools=[toolbox],
)
