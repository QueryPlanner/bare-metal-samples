from pathlib import Path

from google.adk.tools import ToolContext, function_tool
from google.genai import types
from PIL import Image


async def fetch_image_tool(image_filename: str, tool_context: ToolContext) -> list[str | types.Part]:
    """Loads a meme template image from the local dataset using its exact filename
    and saves it as an artifact.

    This tool returns the image directly to you and also saves it as an artifact.
    You do NOT need to call 'load_artifacts' after this tool.

    Args:
        image_filename: The exact filename of the meme image (e.g., 'Doge.jpg', '10-Guy.jpg').
                       This MUST be obtained from the 'image_filename' field of
                       the 'meme_info_tool'.
        tool_context: Internal context for artifact management.

    Returns:
        A list containing a success message and the image data as a Part.
    """
    if not image_filename:
        return ["Error: No image filename provided."]

    # Base directory for meme images
    images_dir = Path("data/meme_dataset/templates/img")

    # Use the filename directly
    image_path = images_dir / image_filename

    if not image_path.exists():
        return [
            f"Error: Meme template image '{image_filename}' not found in {images_dir}. "
            "Please ensure you are using the 'image_filename' exactly as provided by "
            "'meme_info_tool'."
        ]

    try:
        # Read the image file
        image_data = image_path.read_bytes()

        # Get image dimensions
        with Image.open(image_path) as img:
            width, height = img.size

        # Determine mime type
        ext = image_path.suffix.lower()
        mime_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        filename = image_path.name

        # Create a Part with inline_data
        artifact_part = types.Part(inline_data=types.Blob(mime_type=mime_type, data=image_data))

        # Save the artifact using tool_context
        # Use filename as the artifact name for easy reference
        version = await tool_context.save_artifact(filename=filename, artifact=artifact_part)

        return [
            (
                f"Successfully loaded '{filename}' from local dataset as artifact "
                f"(version {version}). Dimensions: {width}x{height} (Width x Height)."
            ),
            artifact_part,
        ]

    except Exception as e:
        return [f"Error loading image: {str(e)}"]


fetch_image_tool = function_tool.FunctionTool(fetch_image_tool)
