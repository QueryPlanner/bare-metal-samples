import os

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

# Import tools and sub-agents
from google.adk.tools import load_artifacts

from .tools.image_editor import add_text_to_image_tool
from .tools.image_fetcher import fetch_image_tool
from .tools.meme_info import meme_info_tool

api_base_url = "https://openrouter.ai/api/v1"

root_agent = Agent(
    model=LiteLlm(
        model="openrouter/google/gemini-3-flash-preview",
        api_base=api_base_url,
        api_key=os.getenv("OPENROUTER_API_KEY"),
    ),
    name="root_agent",
    description=(
        "A helpful assistant for user questions, including meme information and image handling."
    ),
    instruction="""
    You are meme agent. Always use 'meme_info_tool' tool as the conversation starts.
    You can load meme template images from the local dataset and save them as artifacts
    using 'fetch_image_tool'.
    To view or analyze saved artifacts (like images), you MUST use 'load_artifacts'.
    Always use the 'load_artifacts' right after 'fetch_image_tool' tool to view the images
    you have saved.
    You can also add text overlays to images using 'add_text_to_image_tool'. Use Impact font 
    and provide locations (top-left coordinates), texts, and font sizes.

    After you create the meme load it again and verify the text and quality, if not good create again.
    """,
    # Register the sub-agent structurally
    # sub_agents=[researcher_agent()],
    # Give the agent tools to do its job (including transferring)
    tools=[meme_info_tool, fetch_image_tool, load_artifacts, add_text_to_image_tool],
)