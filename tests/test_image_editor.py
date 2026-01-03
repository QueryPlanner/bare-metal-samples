import sys
import io
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from agents.meme_agent.tools.image_editor import add_text_to_image_tool, add_text_to_image
from google.adk.tools.tool_context import ToolContext
from PIL import Image

async def test_add_text_to_image_success():
    # Setup
    tool_context = MagicMock(spec=ToolContext)
    tool_context.save_artifact = AsyncMock(return_value="v1")
    
    with patch("agents.meme_agent.tools.image_editor.Path.exists", return_value=True), \
         patch("agents.meme_agent.tools.image_editor.Image.open") as mock_open:
        
        # Create a mock image
        mock_img = MagicMock()
        mock_img.mode = "RGB"
        mock_img.size = (100, 100)
        
        def side_effect_save(fp, format):
            fp.write(b"fake_image_data")
        
        mock_img.save.side_effect = side_effect_save
        mock_open.return_value.__enter__.return_value = mock_img
        
        # Execute with 2 text overlays
        result = await add_text_to_image(
            image_filename="Test.jpg",
            text_locations=[[10, 10], [60, 60]],
            texts=["Meme 1", "Meme 2"],
            font_sizes=[20, 15],
            tool_context=tool_context
        )
        
        # Verify
        assert "Successfully added 2 text overlays" in result
        assert "Test.jpg" in result
        tool_context.save_artifact.assert_called_once()
        
        # Verify args to save_artifact
        call_kwargs = tool_context.save_artifact.call_args.kwargs
        assert call_kwargs['filename'] == "text_added_Test.jpg"
        assert call_kwargs['artifact'].inline_data.mime_type == "image/jpeg"

async def test_add_text_to_image_invalid_loc_format():
    tool_context = MagicMock(spec=ToolContext)
    
    with patch("agents.meme_agent.tools.image_editor.Path.exists", return_value=True), \
         patch("agents.meme_agent.tools.image_editor.Image.open") as mock_open:
         
        mock_img = MagicMock()
        mock_img.mode = "RGB"
        mock_open.return_value.__enter__.return_value = mock_img

        result = await add_text_to_image(
            image_filename="Test.jpg",
            text_locations=[[10]], # Invalid inner list length
            texts=["Test"],
            font_sizes=[10],
            tool_context=tool_context
        )
        
    assert "Error: Invalid location" in result

async def test_add_text_to_image_mismatch_lengths():
    tool_context = MagicMock(spec=ToolContext)
    
    result = await add_text_to_image(
        image_filename="Test.jpg",
        text_locations=[[10, 10]],
        texts=["Test"],
        font_sizes=[10, 20], # Mismatch length
        tool_context=tool_context
    )
    
    assert "Error: The number of locations, texts, and font_sizes must match" in result

async def test_add_text_to_image_too_many():
    tool_context = MagicMock(spec=ToolContext)
    
    locs = [[0,0]] * 5
    texts = ["t"] * 5
    sizes = [10] * 5
    
    result = await add_text_to_image(
        image_filename="Test.jpg",
        text_locations=locs,
        texts=texts,
        font_sizes=sizes,
        tool_context=tool_context
    )
    
    assert "Error: You can provide at most 4 text overlays" in result

async def test_add_text_to_image_no_file():
    tool_context = MagicMock(spec=ToolContext)
    
    with patch("agents.meme_agent.tools.image_editor.Path.exists", return_value=False):
        result = await add_text_to_image(
            image_filename="NonExistent.jpg",
            text_locations=[[0,0]],
            texts=["Test"],
            font_sizes=[10],
            tool_context=tool_context
        )
        
    assert "Error: Image 'NonExistent.jpg' not found" in result
