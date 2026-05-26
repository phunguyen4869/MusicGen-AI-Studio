import requests
import json
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file, going up one directory level
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

url = "https://api.minimax.io/v1/music_generation"
api_key = os.environ.get("MINIMAX_API_KEY")

if not api_key:
    print("Error: MINIMAX_API_KEY environment variable not set.")
    print("Please set it in your .env file or environment variables.")
    sys.exit(1)

# Try to load the cover_feature_id from the context file created by preprocess.py
try:
    with open("cover_context.json", "r", encoding="utf-8") as f:
        context = json.load(f)
        cover_feature_id = context.get("cover_feature_id")
except FileNotFoundError:
    print("Error: cover_context.json not found. Please run preprocess.py first.")
    # Fallback to hardcoded value for demonstration if file doesn't exist
    # cover_feature_id = "your_feature_id_here"
    sys.exit(1)

if not cover_feature_id:
    print("Error: Valid cover_feature_id not found in context.")
    sys.exit(1)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Modify the extracted lyrics as needed
modified_lyrics = "[Verse 1]\nYour modified first verse here\nWith new words that tell your story\n\n[Chorus]\nA brand new chorus for the cover\nSinging with a different feel"

payload = {
    "model": "music-cover",
    "cover_feature_id": cover_feature_id,
    "lyrics": modified_lyrics,
    "prompt": "Jazz, smooth, late night lounge, saxophone",
    "audio_setting": {
        "sample_rate": 44100,
        "bitrate": 256000,
        "format": "mp3"
    },
    "output_format": "url"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    print(json.dumps(result, ensure_ascii=False, indent=2))
except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
    if hasattr(e, 'response') and e.response is not None:
        try:
            print(f"Error response from server: {e.response.json()}")
        except ValueError:
            print(f"Error response from server: {e.response.text}")