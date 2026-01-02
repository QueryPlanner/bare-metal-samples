import os
from pathlib import Path
from google.adk.tools import function_tool, ToolContext
from google.genai import types
from typing import Optional, Union

async def load_meme_image_to_artifact(meme_name: str, tool_context: ToolContext) -> str:
    """
    Loads a meme template image from the local dataset and saves it as an artifact.
    
    Args:
        meme_name: The name of the meme (e.g., '10-Guy', 'Doge'). 
                  This should match the filename in data/meme_dataset/templates/img.
        tool_context: Internal context for artifact management.
        
    Returns:
        A success message or an error message.
    """
    # Base directory for meme images
    images_dir = Path("data/meme_dataset/templates/img")
    
    # Try to find the file with common extensions
    possible_extensions = [".jpg", ".png", ".jpeg"]
    image_path = None
    
    # Normalize meme_name (strip whitespace, etc.)
    meme_name = meme_name.strip().lower()
    
    # Robust matching: iterate all files in images_dir
    for file in images_dir.iterdir():
        if file.is_file() and file.suffix.lower() in possible_extensions:
            stem_lower = file.stem.lower()
            # Exact match (case-insensitive)
            if stem_lower == meme_name:
                image_path = file
                break
            # Substring match if exact match not found yet
            if not image_path and meme_name in stem_lower:
                image_path = file

    if not image_path:
        return f"Error: Meme template image for '{meme_name}' not found in {images_dir}."

    try:
        # Read the image file
        image_data = image_path.read_bytes()
        
        # Determine mime type
        ext = image_path.suffix.lower()
        mime_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        
        filename = image_path.name
        
        # Create a Part with inline_data
        artifact_part = types.Part(
            inline_data=types.Blob(
                mime_type=mime_type,
                data=image_data
            )
        )
        
        # Save the artifact using tool_context
        # Use filename as the artifact name for easy reference
        version = await tool_context.save_artifact(
            filename=filename,
            artifact=artifact_part
        )
        
        return f"Successfully loaded '{filename}' from local dataset as artifact (version {version}). You can now use 'load_artifacts' to view it."
            
    except Exception as e:
        return f"Error loading image: {str(e)}"

fetch_image_tool = function_tool.FunctionTool(load_meme_image_to_artifact)