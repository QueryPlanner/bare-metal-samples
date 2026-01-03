import io
from pathlib import Path

from google.adk.tools import ToolContext, function_tool
from google.genai import types
from PIL import Image, ImageDraw, ImageFont


async def draw_bounding_box(
    image_filename: str,
    boxes: list[list[int]],
    texts: list[str],
    font_sizes: list[int],
    tool_context: ToolContext
) -> str:
    """
    Draws up to 4 bounding boxes with text of specified sizes on a meme template image.

    Args:
        image_filename: The filename of the image (must be in data/meme_dataset/templates/img).
        boxes: A list of bounding boxes, where each box is a list of 4 integers 
            [x_min, y_min, x_max, y_max]. Max 4 boxes.
        texts: A list of strings corresponding to each box.
        font_sizes: A list of integers specifying the font size for each text.
        tool_context: Internal context for artifact management.

    Returns:
        A success message indicating the image has been processed and saved as an artifact.
    """
    if not image_filename:
        return "Error: No image filename provided."
    
    if not boxes or not texts or not font_sizes:
         return "Error: boxes, texts, and font_sizes must be provided."

    if len(boxes) > 4:
        return "Error: You can provide at most 4 bounding boxes."

    if not (len(boxes) == len(texts) == len(font_sizes)):
        return "Error: The number of boxes, texts, and font_sizes must match."

    # Base directory for meme images
    images_dir = Path("data/meme_dataset/templates/img")
    image_path = images_dir / image_filename

    if not image_path.exists():
        return f"Error: Image '{image_filename}' not found in {images_dir}."

    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary to ensure drawing works as expected
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            draw = ImageDraw.Draw(img)
            
            for box, text, size in zip(boxes, texts, font_sizes):
                if len(box) != 4:
                    return f"Error: Invalid box coordinates {box}. Must be [x_min, y_min, x_max, y_max]."
                
                # Draw bounding box
                # Outline color red, width 3
                draw.rectangle(box, outline="red", width=3)
                
                # Load font with specified size
                try:
                    font = ImageFont.load_default(size=size)
                except TypeError:
                     # Fallback for older Pillow versions if size param not supported (though we have 12.1.0)
                     font = ImageFont.load_default()

                # Position text at the top-left of the box
                text_position = (box[0] + 5, box[1] + 5)
                
                # Draw text with a background for visibility
                bbox = draw.textbbox(text_position, text, font=font)
                draw.rectangle(bbox, fill="black")
                draw.text(text_position, text, fill="white", font=font)
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="JPEG")
            img_byte_arr.seek(0)
            image_data = img_byte_arr.read()
            
            # Create artifact
            filename = f"annotated_{image_filename}"
            artifact_part = types.Part(
                inline_data=types.Blob(mime_type="image/jpeg", data=image_data)
            )

            version = await tool_context.save_artifact(
                filename=filename, artifact=artifact_part
            )

            return (
                f"Successfully drew {len(boxes)} bounding boxes and texts on '{image_filename}'. "
                f"Saved as artifact '{filename}' (version {version}). "
                "Use 'load_artifacts' to view it."
            )

    except Exception as e:
        return f"Error processing image: {str(e)}"

draw_bounding_box_tool = function_tool.FunctionTool(draw_bounding_box)
