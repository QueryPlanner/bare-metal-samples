import json
import random
from pathlib import Path
from typing import List, Dict, Any
from google.adk.tools import function_tool

def get_meme_templates_info() -> List[Dict[str, Any]]:
    """
    Retrieves information about all meme templates.
    
    Returns:
        A list of dictionaries, each containing:
        - name: The title of the meme template.
        - alternative_names: Alternative names for the meme.
        - examples: 3 randomly sampled example boxes for that meme.
    """
    # Use relative paths from the project root
    templates_dir = Path("data/meme_dataset/templates")
    memes_dir = Path("data/meme_dataset/memes")
    
    results = []
    
    if not templates_dir.exists():
        return []

    for template_file in sorted(templates_dir.glob("*.json")):
        try:
            with open(template_file, "r") as f:
                template_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue
        
        name = template_data.get("title", template_file.stem)
        # Clean up title if it ends with " Meme Template"
        if name.endswith(" Meme Template"):
            name = name[:-14]
            
        alt_names = template_data.get("alternative_names", "")
        
        meme_file = memes_dir / template_file.name
        examples = []
        if meme_file.exists():
            try:
                with open(meme_file, "r") as f:
                    meme_data = json.load(f)
                
                if isinstance(meme_data, list) and meme_data:
                    sample_size = min(len(meme_data), 3)
                    sampled_memes = random.sample(meme_data, sample_size)
                    for m in sampled_memes:
                        if isinstance(m, dict) and "boxes" in m:
                            examples.append(m["boxes"])
            except (json.JSONDecodeError, IOError):
                pass
        
        results.append({
            "name": name,
            "alternative_names": alt_names,
            "examples": examples
        })
    
    return results

meme_info_tool = function_tool.FunctionTool(get_meme_templates_info)
