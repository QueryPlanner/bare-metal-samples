import io
from pathlib import Path

from google.adk.tools import ToolContext, function_tool
from google.genai import types
from PIL import Image, ImageDraw, ImageFont


async def add_text_to_image(
    image_filename: str,
    text_locations: list[list[int]],
    texts: list[str],
    font_sizes: list[int],
    tool_context: ToolContext
) -> str:
    """
    Adds up to 4 text overlays on a meme template image using Impact font.

    Args:
        image_filename: The filename of the image (must be in data/meme_dataset/templates/img).
        text_locations: A list of locations, where each location is a list of 2 or 4 integers 
            [x, y] or [x_min, y_min, x_max, y_max]. If 4 integers, top-left is used. Max 4.
        texts: A list of strings corresponding to each location.
        font_sizes: A list of integers specifying the font size for each text.
        tool_context: Internal context for artifact management.

    Returns:
        A success message indicating the image has been processed and saved as an artifact.
    """
    if not image_filename:
        return "Error: No image filename provided."
    
    if not text_locations or not texts or not font_sizes:
         return "Error: text_locations, texts, and font_sizes must be provided."

    if len(text_locations) > 4:
        return "Error: You can provide at most 4 text overlays."

    if not (len(text_locations) == len(texts) == len(font_sizes)):
        return "Error: The number of locations, texts, and font_sizes must match."

    # Base directory for meme images
    images_dir = Path("data/meme_dataset/templates/img")
    image_path = images_dir / image_filename

    if not image_path.exists():
        return f"Error: Image '{image_filename}' not found in {images_dir}."

    # Font path
    font_path = "Impact.ttf"

    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary to ensure drawing works as expected
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            draw = ImageDraw.Draw(img)
            
            for loc, text, size in zip(text_locations, texts, font_sizes):
                if len(loc) not in [2, 4]:
                    return f"Error: Invalid location {loc}. Must be [x, y] or [x_min, y_min, x_max, y_max]."
                
                # Use Impact font if available
                try:
                    font = ImageFont.truetype(font_path, size=size)
                except Exception:
                     # Fallback to default if Impact.ttf fails for some reason
                     try:
                         font = ImageFont.load_default(size=size)
                     except TypeError:
                         font = ImageFont.load_default()

                # Position text at the top-left of the provided location
                text_position = (loc[0], loc[1])
                
                # Draw black text (no background, no bounding box)
                draw.text(text_position, text, fill="black", font=font)
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="JPEG")
            img_byte_arr.seek(0)
            image_data = img_byte_arr.read()
            
            # Create artifact
            filename = f"text_added_{image_filename}"
            artifact_part = types.Part(
                inline_data=types.Blob(mime_type="image/jpeg", data=image_data)
            )

            version = await tool_context.save_artifact(
                filename=filename, artifact=artifact_part
            )

            return (
                f"Successfully added {len(texts)} text overlays on '{image_filename}'. "
                f"Saved as artifact '{filename}' (version {version}). "
                "Use 'load_artifacts' to view it."
            )

    except Exception as e:
        return f"Error processing image: {str(e)}"

add_text_to_image_tool = function_tool.FunctionTool(add_text_to_image)