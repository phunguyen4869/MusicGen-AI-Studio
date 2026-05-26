# MiniMax Music Generation Example

This repository contains a simple Python script to generate music using the [MiniMax Music 2.6 API](https://platform.minimax.io/docs/guides/music-generation).

## Prerequisites

- Python 3.x
- MiniMax API Key (get one from the [MiniMax Platform](https://platform.minimax.io/))

## Setup

1. Clone or download this repository.
2. Navigate to the project directory.
3. Set up a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Copy the example environment file and add your API key:

```bash
cp .env.example .env
```
Edit the `.env` file and replace `your_api_key_here` with your actual MiniMax API key.

## Usage

Run the script to generate a song based on the predefined prompt and lyrics:

```bash
python music_generation.py
```

The script will output a JSON response containing the generated audio URL and other metadata if successful.

## Customization

You can edit `music_generation.py` to change the `prompt` or `lyrics` to generate different styles of music or different songs. You can also use the `is_instrumental: true` flag in the payload for instrumental tracks, or enable `lyrics_optimizer: true` to have the AI write the lyrics for you based on the prompt.