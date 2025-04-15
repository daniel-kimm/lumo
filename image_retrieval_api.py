#!/usr/bin/env python
import sys
import json
from image_retrieval import create_moodboard

def main():
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Prompt argument is required"}))
        sys.exit(1)
    
    prompt = sys.argv[1]
    
    try:
        # Get images for the moodboard
        images = create_moodboard(prompt, num_images=16)
        
        # Convert to JSON and print to stdout
        print(json.dumps(images))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main() 