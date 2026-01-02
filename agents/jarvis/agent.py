import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

# Import tools and sub-agents
from google.adk.tools import load_artifacts
from .tools.meme_info import meme_info_tool
from .tools.image_fetcher import fetch_image_tool
from .sub_agents.researcher import researcher_agent

api_base_url = "https://openrouter.ai/api/v1"

root_agent = Agent(
    model=LiteLlm(
        model="openrouter/google/gemini-2.5-flash-lite",
        api_base=api_base_url,
        api_key=os.getenv("OPENROUTER_API_KEY"),
    ),
    name="root_agent",
    description="A helpful assistant for user questions, including meme information and image handling.",
    instruction="""
    Answer user questions to the best of your knowledge.
    You can use the 'researcher' agent for complex topics by using the transfer tool.
    You can retrieve information about meme templates and examples using the 'meme_info_tool'.
    You can load meme template images from the local dataset and save them as artifacts using 'fetch_image_tool'.
    To view or analyze saved artifacts (like images), you MUST use 'load_artifacts'.
    """,
    # Register the sub-agent structurally
    sub_agents=[researcher_agent()],
    # Give the agent tools to do its job (including transferring)
    tools=[meme_info_tool, fetch_image_tool, load_artifacts],
)