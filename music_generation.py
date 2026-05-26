import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

url = os.environ.get("MINIMAX_API_URL_MUSIC", "https://api.minimax.io/v1/music_generation")
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
    "model": "music-2.6",
    "prompt": "Progressive metal, 7/8 beats, tight rhythm, beat down, sickness guitar solo",
    "lyrics": "Bleh",
    "audio_setting": {
        "sample_rate": 44100,
        "bitrate": 256000,
        "format": "mp3"
    },
    "output_format": "url"
}

try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status() # Raise an exception for bad status codes
    result = response.json()
    print(json.dumps(result, ensure_ascii=False, indent=2))
except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
    if hasattr(e, 'response') and e.response is not None:
        try:
            print(f"Error response from server: {e.response.json()}")
        except ValueError:
            print(f"Error response from server: {e.response.text}")