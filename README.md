# MiniMax AI Studio (Music + Image + Speech)

A Streamlit app that integrates multiple MiniMax APIs in one place:

- Lyric generation
- Music generation
- Cover generation (preprocess + regenerate)
- Text to Image generation
- Text to Speech generation

## Features

- Sidebar authentication (`APP_USERNAME` / `APP_PASSWORD`)
- API key input in UI (`MINIMAX_API_KEY`)
- Modular architecture for feature tabs:
  - `image_generation.py`
  - `tts_generation.py`
- Raw JSON response viewer for easier debugging

## Prerequisites

- Python 3.9+
- MiniMax API key from [MiniMax Platform](https://platform.minimax.io/)

## Setup

1. Clone repository and open project folder.
2. Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
cp .env.example .env
```

Then update `.env` with your values.

## Environment variables

Minimum required:

- `MINIMAX_API_KEY`
- `APP_USERNAME`
- `APP_PASSWORD`

Optional endpoint overrides:

- `MINIMAX_API_URL_LYRICS` (default: `https://api.minimax.io/v1/lyrics_generation`)
- `MINIMAX_API_URL_MUSIC` (default: `https://api.minimax.io/v1/music_generation`)
- `MINIMAX_API_URL_IMAGE` (default: `https://api.minimax.io/v1/image_generation`)
- `MINIMAX_API_URL_TTS` (default: `https://api.minimax.io/v1/t2a_v2`)

## Run app

```bash
streamlit run app.py
```

Open the local Streamlit URL shown in terminal, login from sidebar, and input your MiniMax API key.

## API references

- Text to Image: [MiniMax Text to Image API](https://platform.minimax.io/docs/api-reference/image-generation-t2i)
- Text to Speech (HTTP): [MiniMax T2A HTTP API](https://platform.minimax.io/docs/api-reference/speech-t2a-http)

## Project structure

- `app.py`: Main Streamlit app and tab routing
- `image_generation.py`: Text-to-image UI + request handling
- `tts_generation.py`: Text-to-speech UI + request handling
- `music_generation.py`: Simple standalone music generation script
- `Cover/preprocess.py`: Cover preprocessing helper script

## Notes

- Some API output URLs may expire after a limited time.
- If a request fails, check the `base_resp.status_code/status_msg` in the expanded raw JSON response.
- Keep `.env` private and never commit secrets.