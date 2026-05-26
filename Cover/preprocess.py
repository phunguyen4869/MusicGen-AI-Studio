import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file, going up one directory level
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

url = "https://api.minimax.io/v1/music_cover_preprocess"
api_key = os.environ.get("MINIMAX_API_KEY")

if not api_key:
    print("Error: MINIMAX_API_KEY environment variable not set.")
    print("Please set it in your .env file or environment variables.")
    exit(1)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "music-cover",
    "audio_url": "https://example.com/original-song.mp3"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    
    # Check if the API returned an error in the JSON response
    if "base_resp" in result and result["base_resp"].get("status_code", 0) != 0:
        print(f"API Error: {json.dumps(result, ensure_ascii=False, indent=2)}")
        exit(1)

    # Save the cover_feature_id and review the lyrics
    cover_feature_id = result.get("cover_feature_id")
    formatted_lyrics = result.get("formatted_lyrics", "No lyrics extracted")

    if cover_feature_id:
        print(f"Feature ID: {cover_feature_id}")
        print(f"Extracted Lyrics:\n{formatted_lyrics}")
        
        # Save to a temporary file for generate_cover.py to use
        with open("cover_context.json", "w", encoding="utf-8") as f:
            json.dump({"cover_feature_id": cover_feature_id}, f)
        print("\nFeature ID saved to cover_context.json for next step.")
    else:
        print(f"Unexpected response format: {json.dumps(result, ensure_ascii=False, indent=2)}")

except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
    if hasattr(e, 'response') and e.response is not None:
        try:
            print(f"Error response from server: {e.response.json()}")
        except ValueError:
            print(f"Error response from server: {e.response.text}")