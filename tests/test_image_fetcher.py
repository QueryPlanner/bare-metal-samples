import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from google.adk.tools.tool_context import ToolContext
from google.genai import types

from agents.meme_agent.tools.image_fetcher import fetch_image_tool


async def test_fetch_image():
    print("Testing fetch_image_tool...")
    
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
    
    # Test meme filename (10 Guy template)
    image_filename = "10-Guy.jpg"

    # Mock Path.exists and read_bytes and Image.open
    from unittest.mock import patch
    with patch("agents.meme_agent.tools.image_fetcher.Path.exists", return_value=True), \
         patch("agents.meme_agent.tools.image_fetcher.Path.read_bytes", return_value=b"fake_image_bytes"), \
         patch("agents.meme_agent.tools.image_fetcher.Image.open") as mock_open:

        # Mock image size
        mock_img = MagicMock()
        mock_img.size = (800, 600)
        mock_open.return_value.__enter__.return_value = mock_img

        result = await fetch_image_tool.func(image_filename, tool_context)
        print(f"Result: {result}")
        
        # Verify save_artifact was called
        if "Successfully loaded" in result:
            print("SUCCESS: Tool reported success.")
            args, kwargs = mock_artifact_service.save_artifact.call_args
            print(f"save_artifact called with filename: {kwargs.get('filename')}")
            if isinstance(kwargs.get('artifact'), types.Part):
                print("SUCCESS: Artifact is a types.Part.")
            
            # Assert dimensions are present
            if "Dimensions: 800x600" in result:
                print("SUCCESS: Dimensions found in result.")
            else:
                print("FAIL: Dimensions NOT found in result.")
                raise AssertionError("Dimensions expected in result")

        else:
            print(f"FAIL: Tool reported error: {result}")
            raise AssertionError(f"Tool failed: {result}")

if __name__ == "__main__":
    asyncio.run(test_fetch_image())
