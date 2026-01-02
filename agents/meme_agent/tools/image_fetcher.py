from pathlib import Path

from google.adk.tools import ToolContext, function_tool
from google.genai import types


async def fetch_image_tool(image_filename: str, tool_context: ToolContext) -> str:
    """Loads a meme template image from the local dataset using its exact filename
    and saves it as an artifact.

    If you have used this tool always call load_artifacts tool to view the images you have saved.
    This tool returns the image directly to user and loads it as an artifact, so user can see
    it but you can't. Therefore, always use the load_artifacts tool.

    Args:
        image_filename: The exact filename of the meme image (e.g., 'Doge.jpg', '10-Guy.jpg').
                       This MUST be obtained from the 'image_filename' field of
                       the 'meme_info_tool'.
        tool_context: Internal context for artifact management.

    Returns:
        A success message or an error message.
    """
    # Base directory for meme images
    images_dir = Path("data/meme_dataset/templates/img")

    # Use the filename directly
    image_path = images_dir / image_filename

    if not image_path.exists():
        return (
            f"Error: Meme template image '{image_filename}' not found in {images_dir}. "
            "Please ensure you are using the 'image_filename' exactly as provided by "
            "'meme_info_tool'."
        )

    try:
        # Read the image file
        image_data = image_path.read_bytes()

        # Determine mime type
        ext = image_path.suffix.lower()
        mime_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        filename = image_path.name

        # Create a Part with inline_data
        artifact_part = types.Part(inline_data=types.Blob(mime_type=mime_type, data=image_data))

        # Save the artifact using tool_context
        # Use filename as the artifact name for easy reference
        version = await tool_context.save_artifact(filename=filename, artifact=artifact_part)

        return (
            f"Successfully loaded '{filename}' from local dataset as artifact "
            f"(version {version}). You can now use 'load_artifacts' to view it."
        )

    except Exception as e:
        return f"Error loading image: {str(e)}"


fetch_image_tool = function_tool.FunctionTool(fetch_image_tool)
