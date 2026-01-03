import sys
import io
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from agents.meme_agent.tools.image_editor import draw_bounding_box_tool, draw_bounding_box
from google.adk.tools.tool_context import ToolContext
from PIL import Image

async def test_draw_bounding_box_success():
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
        
        # Execute with 2 boxes
        result = await draw_bounding_box(
            image_filename="Test.jpg",
            boxes=[[10, 10, 50, 50], [60, 60, 90, 90]],
            texts=["Meme 1", "Meme 2"],
            font_sizes=[20, 15],
            tool_context=tool_context
        )
        
        # Verify
        assert "Successfully drew 2 bounding boxes" in result
        assert "Test.jpg" in result
        tool_context.save_artifact.assert_called_once()
        
        # Verify args to save_artifact
        call_kwargs = tool_context.save_artifact.call_args.kwargs
        assert call_kwargs['filename'] == "annotated_Test.jpg"
        assert call_kwargs['artifact'].inline_data.mime_type == "image/jpeg"

async def test_draw_bounding_box_invalid_box_format():
    tool_context = MagicMock(spec=ToolContext)
    
    with patch("agents.meme_agent.tools.image_editor.Path.exists", return_value=True), \
         patch("agents.meme_agent.tools.image_editor.Image.open") as mock_open:
         
        mock_img = MagicMock()
        mock_img.mode = "RGB"
        mock_open.return_value.__enter__.return_value = mock_img

        result = await draw_bounding_box(
            image_filename="Test.jpg",
            boxes=[[10, 10]], # Invalid inner list length
            texts=["Test"],
            font_sizes=[10],
            tool_context=tool_context
        )
        
    assert "Error: Invalid box coordinates" in result

async def test_draw_bounding_box_mismatch_lengths():
    tool_context = MagicMock(spec=ToolContext)
    
    result = await draw_bounding_box(
        image_filename="Test.jpg",
        boxes=[[10, 10, 50, 50]],
        texts=["Test"],
        font_sizes=[10, 20], # Mismatch length (2 vs 1)
        tool_context=tool_context
    )
    
    assert "Error: The number of boxes, texts, and font_sizes must match" in result

async def test_draw_bounding_box_too_many():
    tool_context = MagicMock(spec=ToolContext)
    
    boxes = [[0,0,1,1]] * 5
    texts = ["t"] * 5
    sizes = [10] * 5
    
    result = await draw_bounding_box(
        image_filename="Test.jpg",
        boxes=boxes,
        texts=texts,
        font_sizes=sizes,
        tool_context=tool_context
    )
    
    assert "Error: You can provide at most 4 bounding boxes" in result

async def test_draw_bounding_box_no_file():
    tool_context = MagicMock(spec=ToolContext)
    
    with patch("agents.meme_agent.tools.image_editor.Path.exists", return_value=False):
        result = await draw_bounding_box(
            image_filename="NonExistent.jpg",
            boxes=[[0,0,10,10]],
            texts=["Test"],
            font_sizes=[10],
            tool_context=tool_context
        )
        
    assert "Error: Image 'NonExistent.jpg' not found" in result