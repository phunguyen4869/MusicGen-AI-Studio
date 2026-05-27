import requests
import streamlit as st
import os


def render_text_to_speech_tab(headers: dict):
    st.header("🗣️ Text to Speech")
    st.info("Convert text to speech with MiniMax T2A HTTP API.")

    text_input = st.text_area(
        "Input Text",
        placeholder="Type text to synthesize...",
        height=160,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        model = st.selectbox(
            "Model",
            [
                "speech-2.8-hd",
                "speech-2.8-turbo",
                "speech-2.6-hd",
                "speech-2.6-turbo",
                "speech-02-hd",
                "speech-02-turbo",
                "speech-01-hd",
                "speech-01-turbo",
            ],
            index=0,
        )
    with col2:
        voice_id = st.text_input("Voice ID", value="English_expressive_narrator")
    with col3:
        language_boost = st.selectbox("Language Boost", ["auto", "English", "Vietnamese"], index=0)

    col4, col5, col6 = st.columns(3)
    with col4:
        speed = st.slider("Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    with col5:
        vol = st.slider("Volume", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
    with col6:
        pitch = st.slider("Pitch", min_value=-12, max_value=12, value=0, step=1)

    if st.button("Generate Speech", key="btn_tts"):
        if not text_input.strip():
            st.error("Please enter text.")
            return

        url = os.environ.get("MINIMAX_API_URL_TTS", "https://api.minimax.io/v1/t2a_v2")
        payload = {
            "model": model,
            "text": text_input,
            "stream": False,
            "language_boost": language_boost,
            "output_format": "hex",
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "vol": vol,
                "pitch": pitch,
            },
            "audio_setting": {
                "sample_rate": 32000,
                "bitrate": 128000,
                "format": "mp3",
                "channel": 1,
            },
        }

        with st.spinner("Generating speech..."):
            try:
                res = requests.post(url, headers=headers, json=payload)
                res.raise_for_status()
                data = res.json()

                if data.get("base_resp", {}).get("status_code", 0) != 0:
                    st.error(f"API Error: {data.get('base_resp', {}).get('status_msg', 'Unknown error')}")
                    st.json(data)
                    return

                audio_hex = data.get("data", {}).get("audio")
                if not audio_hex:
                    st.warning("No audio field found in response.")
                    st.json(data)
                    return

                audio_bytes = bytes.fromhex(audio_hex)
                st.success("Speech generated successfully!")
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button("Download MP3", data=audio_bytes, file_name="tts_output.mp3", mime="audio/mpeg")

                with st.expander("Show raw JSON response"):
                    st.json(data)
            except Exception as e:
                st.error(f"Error: {e}")
                if hasattr(e, "response") and e.response is not None:
                    try:
                        st.json(e.response.json())
                    except Exception:
                        st.text(e.response.text)
