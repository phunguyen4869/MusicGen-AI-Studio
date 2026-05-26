import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App layout & styling
st.set_page_config(page_title="MusicGen AI Studio", page_icon="🎵", layout="wide")
st.title("🎵 MusicGen AI Studio")
st.markdown("Generate music, write lyrics, and cover songs with AI (Minimax API).")

# Setup API Key
api_key = os.environ.get("MINIMAX_API_KEY", "")

# Simple Authentication System
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Sidebar for Authentication & Settings
with st.sidebar:
    st.header("🔐 Authentication")
    
    if not st.session_state.authenticated:
        st.info("Please login to use the application.")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Hardcoded credentials for demonstration (can be moved to .env later)
        VALID_USER = os.environ.get("APP_USERNAME", "admin")
        VALID_PASS = os.environ.get("APP_PASSWORD", "admin123")
        
        if st.button("Login", use_container_width=True):
            if username == VALID_USER and password == VALID_PASS:
                st.session_state.authenticated = True
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    else:
        st.success("✅ Logged in")
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
            
        st.divider()
        st.header("⚙️ Settings")
        user_api_key = st.text_input("Minimax API Key", value=api_key, type="password")

# Block access if not authenticated
if not st.session_state.authenticated:
    st.warning("⚠️ Please login from the sidebar to access the AI Studio.")
    st.stop()

if not user_api_key:
    st.warning("⚠️ Please enter your Minimax API Key in the sidebar to continue.")
    st.stop()

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {user_api_key}"
}

# Tabs for features
tab1, tab2, tab3 = st.tabs(["📝 Lyric Generation", "🎸 Music Generation", "🎧 Cover Generation"])

# --- TAB 1: LYRIC GENERATION ---
with tab1:
    st.header("📝 Lyric Generator")
    lyric_prompt = st.text_area("Enter your prompt for lyrics", placeholder="Example: A soulful blues song about a rainy night...")
    
    if st.button("Generate Lyrics", key="btn_lyric"):
        if not lyric_prompt:
            st.error("Please enter a prompt!")
        else:
            with st.spinner("Generating lyrics..."):
                url = os.environ.get("MINIMAX_API_URL_LYRICS", "https://api.minimax.io/v1/lyrics_generation")
                payload = {
                    "mode": "write_full_song",
                    "prompt": lyric_prompt
                }
                try:
                    res = requests.post(url, json=payload, headers=headers)
                    res.raise_for_status()
                    data = res.json()
                    st.success("Successfully generated!")
                    st.json(data)
                except Exception as e:
                    st.error(f"Error: {e}")
                    if hasattr(e, 'response') and e.response is not None:
                        st.json(e.response.json())

# --- TAB 2: MUSIC GENERATION ---
with tab2:
    st.header("🎸 Music Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        music_prompt = st.text_area("Genre & Melody (Prompt)", placeholder="Example: Progressive metal, 7/8 beats, tight rhythm...")
    with col2:
        music_lyrics = st.text_area("Lyrics", placeholder="Enter the lyrics here...", height=150)
    
    if st.button("Generate Music", key="btn_music"):
        if not music_prompt:
            st.error("Please enter a prompt for the music!")
        else:
            with st.spinner("Generating music... this may take a while."):
                url = os.environ.get("MINIMAX_API_URL_MUSIC", "https://api.minimax.io/v1/music_generation")
                payload = {
                    "model": "music-2.6",
                    "prompt": music_prompt,
                    "lyrics": music_lyrics,
                    "audio_setting": {
                        "sample_rate": 44100,
                        "bitrate": 256000,
                        "format": "mp3"
                    },
                    "output_format": "url"
                }
                try:
                    res = requests.post(url, headers=headers, json=payload)
                    res.raise_for_status()
                    data = res.json()
                    st.success("Music generated successfully!")
                    
                    # Try to extract audio URL from Minimax response format and play it
                    try:
                        # Assuming the API returns a URL in the response
                        # Minimax response structure might have data -> audio -> url or similar
                        # Example: data = {"audio": "https://url.mp3", ...}
                        
                        audio_url = None
                        
                        # Handle different possible response structures from Minimax API
                        if "data" in data and isinstance(data["data"], dict) and "audio" in data["data"]:
                            audio_url = data["data"]["audio"]
                        elif "audio_url" in data:
                            audio_url = data["audio_url"]
                        elif "url" in data:
                            audio_url = data["url"]
                            
                        if audio_url:
                            st.audio(audio_url, format="audio/mp3")
                        else:
                            st.info("Audio URL not found in response. You can view the raw JSON below.")
                    except Exception as e:
                        st.info("Could not extract audio player from response. Showing raw JSON.")
                        
                    with st.expander("Show raw JSON response"):
                        st.json(data)
                except Exception as e:
                    st.error(f"Error: {e}")
                    if hasattr(e, 'response') and e.response is not None:
                        st.json(e.response.json())

# --- TAB 3: COVER GENERATION ---
with tab3:
    st.header("🎧 Cover Generation (Preprocess & Generate)")
    st.info("Step 1: Enter the original song URL for AI analysis. Step 2: Modify lyrics or genre to create a new cover.")
    
    st.subheader("1️⃣ Preprocess")
    audio_url = st.text_input("Original Song File URL (MP3/WAV)", placeholder="https://example.com/original-song.mp3")
    
    if 'cover_feature_id' not in st.session_state:
        st.session_state.cover_feature_id = None
    if 'formatted_lyrics' not in st.session_state:
        st.session_state.formatted_lyrics = ""
        
    if st.button("Analyze Song", key="btn_preprocess"):
        if not audio_url:
            st.error("Please enter a song file URL!")
        else:
            with st.spinner("Analyzing song..."):
                url = "https://api.minimax.io/v1/music_cover_preprocess"
                payload = {
                    "model": "music-cover",
                    "audio_url": audio_url
                }
                try:
                    res = requests.post(url, headers=headers, json=payload)
                    res.raise_for_status()
                    data = res.json()
                    
                    if "base_resp" in data and data["base_resp"].get("status_code", 0) != 0:
                        st.error(f"API Error: {data['base_resp']}")
                    else:
                        st.session_state.cover_feature_id = data.get("cover_feature_id")
                        st.session_state.formatted_lyrics = data.get("formatted_lyrics", "")
                        st.success(f"Analyzed successfully! Feature ID: {st.session_state.cover_feature_id}")
                except Exception as e:
                    st.error(f"Error: {e}")
                    
    st.divider()
    
    st.subheader("2️⃣ Generate Cover")
    if not st.session_state.cover_feature_id:
        st.warning("Please complete Step 1 (Analyze) before generating a cover.")
    else:
        st.write(f"**Using Feature ID:** `{st.session_state.cover_feature_id}`")
        
        col3, col4 = st.columns(2)
        with col3:
            cover_prompt = st.text_area("New Cover Genre (Prompt)", placeholder="Jazz, smooth, late night lounge, saxophone...")
        with col4:
            modified_lyrics = st.text_area("Modified Lyrics", value=st.session_state.formatted_lyrics, height=200)
            
        if st.button("Generate Cover", key="btn_cover"):
            with st.spinner("Generating new cover..."):
                url = "https://api.minimax.io/v1/music_generation"
                payload = {
                    "model": "music-cover",
                    "cover_feature_id": st.session_state.cover_feature_id,
                    "lyrics": modified_lyrics,
                    "prompt": cover_prompt,
                    "audio_setting": {
                        "sample_rate": 44100,
                        "bitrate": 256000,
                        "format": "mp3"
                    },
                    "output_format": "url"
                }
                try:
                    res = requests.post(url, headers=headers, json=payload)
                    res.raise_for_status()
                    data = res.json()
                    st.success("Cover generated successfully!")
                    
                    # Try to extract audio URL and play it
                    try:
                        audio_url = None
                        if "data" in data and isinstance(data["data"], dict) and "audio" in data["data"]:
                            audio_url = data["data"]["audio"]
                        elif "audio_url" in data:
                            audio_url = data["audio_url"]
                        elif "url" in data:
                            audio_url = data["url"]
                            
                        if audio_url:
                            st.audio(audio_url, format="audio/mp3")
                        else:
                            st.info("Audio URL not found in response.")
                    except Exception as e:
                        pass
                        
                    with st.expander("Show raw JSON response"):
                        st.json(data)
                except Exception as e:
                    st.error(f"Error: {e}")
                    if hasattr(e, 'response') and e.response is not None:
                        st.json(e.response.json())
