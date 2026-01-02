import sys
from pathlib import Path

# Add project root to sys.path to import agents
sys.path.append(str(Path(__file__).parent.parent))

from agents.jarvis.tools.meme_info import get_meme_templates_info

def test_get_meme_templates_info():
    print("Testing get_meme_templates_info...")
    results = get_meme_templates_info()
    
    if not results:
        print("FAIL: No results returned.")
        return

    print(f"SUCCESS: Retrieved {len(results)} meme templates.")
    
    # Check first 3 results
    for i, item in enumerate(results[:3]):
        print(f"\nTemplate {i+1}:")
        print(f"  Name: {item['name']}")
        print(f"  Alt Names: {item['alternative_names']}")
        print(f"  Examples (up to 3):")
        for j, example in enumerate(item['examples']):
            print(f"    {j+1}: {example}")

if __name__ == "__main__":
    test_get_meme_templates_info()
