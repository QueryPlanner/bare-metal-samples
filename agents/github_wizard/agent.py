import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

# Import tools
from .tools.github_mcp import github_mcp_tools

api_base_url = "https://openrouter.ai/api/v1"

root_agent = Agent(
    model=LiteLlm(
        model="openrouter/openai/gpt-oss-120b",
        api_base=api_base_url,
        api_key=os.getenv("OPENROUTER_API_KEY"),
    ),
    name="github_wizard",
    description="A helpful assistant for GitHub related tasks.",
    instruction="""
    Answer user questions to the best of your knowledge using the provided GitHub tools.
    """,
    # Give the agent tools to do its job
    tools=github_mcp_tools,
)
