import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

url = os.environ.get("MINIMAX_API_URL_LYRICS", "https://api.minimax.io/v1/lyrics_generation")
api_key = os.environ.get("MINIMAX_API_KEY")

if not api_key:
    print("Error: MINIMAX_API_KEY environment variable not set.")
    print("Please set it in your .env file or environment variables.")
    exit(1)

payload = {
    "mode": "write_full_song",
    "prompt": "A soulful blues song about a rainy night"
}
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

try:
    response = requests.post(url, json=payload, headers=headers)
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