import json
import random
from pathlib import Path
from typing import Any

from google.adk.tools import function_tool


def meme_info_tool() -> list[dict[str, Any]]:
    """
    Retrieves information about all available meme templates, including their exact image filenames.
    Always use this tool first before answering any questions.
    
    Returns:
        A list of dictionaries, each containing:
        - name: The title of the meme template.
        - image_filename: The exact filename (e.g., 'Doge.jpg') to be used with 'fetch_image_tool' to load the image.
        - alternative_names: Alternative names for the meme.
        - examples: 3 randomly sampled example boxes for that meme.
    """
    # Use relative paths from the project root
    templates_dir = Path("data/meme_dataset/templates")
    images_dir = templates_dir / "img"
    memes_dir = Path("data/meme_dataset/memes")
    
    results = []
    
    if not templates_dir.exists():
        return []

    # Supported image extensions
    image_extensions = [".jpg", ".png", ".jpeg"]

    for template_file in sorted(templates_dir.glob("*.json")):
        try:
            with open(template_file) as f:
                template_data = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        
        stem = template_file.stem
        name = template_data.get("title", stem)
        # Clean up title if it ends with " Meme Template"
        if name.endswith(" Meme Template"):
            name = name[:-14]
            
        alt_names = template_data.get("alternative_names", "")
        
        # Find the actual image filename
        image_filename = None
        if images_dir.exists():
            for ext in image_extensions:
                img_path = images_dir / f"{stem}{ext}"
                if img_path.exists():
                    image_filename = img_path.name
                    break
        
        meme_file = memes_dir / template_file.name
        examples = []
        if meme_file.exists():
            try:
                with open(meme_file) as f:
                    meme_data = json.load(f)
                
                if isinstance(meme_data, list) and meme_data:
                    sample_size = min(len(meme_data), 3)
                    sampled_memes = random.sample(meme_data, sample_size)
                    for m in sampled_memes:
                        if isinstance(m, dict) and "boxes" in m:
                            examples.append(m["boxes"])
            except (OSError, json.JSONDecodeError):
                pass
        
        results.append({
            "name": name,
            "image_filename": image_filename,
            "alternative_names": alt_names,
            "examples": examples
        })
    
    return results

meme_info_tool = function_tool.FunctionTool(meme_info_tool)
