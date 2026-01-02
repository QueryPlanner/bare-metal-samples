import asyncio
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from agents.jarvis.tools.image_fetcher import load_meme_image_to_artifact
from google.adk.tools.tool_context import ToolContext
from google.genai import types

async def test_fetch_image():
    print("Testing load_meme_image_to_artifact...")
    
    # Mock InvocationContext
    mock_invocation_context = MagicMock()
    mock_invocation_context.app_name = "test_app"
    mock_invocation_context.user_id = "test_user"
    mock_invocation_context.session.id = "test_session"
    
    # Mock ArtifactService
    mock_artifact_service = AsyncMock()
    mock_artifact_service.save_artifact.return_value = 1
    mock_invocation_context.artifact_service = mock_artifact_service
    
    # Create ToolContext with mocked InvocationContext
    tool_context = ToolContext(invocation_context=mock_invocation_context)
    
    # Test meme name (10 Guy template)
    meme_name = "10-Guy"
    
    result = await load_meme_image_to_artifact(meme_name, tool_context)
    print(f"Result: {result}")
    
    # Verify save_artifact was called
    if "Successfully loaded" in result:
        print("SUCCESS: Tool reported success.")
        args, kwargs = mock_artifact_service.save_artifact.call_args
        print(f"save_artifact called with filename: {kwargs.get('filename')}")
        if isinstance(kwargs.get('artifact'), types.Part):
            print("SUCCESS: Artifact is a types.Part.")
    else:
        print(f"FAIL: Tool reported error: {result}")

if __name__ == "__main__":
    asyncio.run(test_fetch_image())
