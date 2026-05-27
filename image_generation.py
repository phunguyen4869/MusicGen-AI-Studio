import os
import requests
import streamlit as st


def render_text_to_image_tab(headers: dict):
    st.header("🖼️ Text to Image Generator")
    st.info("Generate images from text using MiniMax Image Generation API.")

    image_prompt = st.text_area(
        "Image Prompt",
        placeholder="Example: A futuristic neon city at night, cinematic lighting, ultra-detailed...",
        height=120,
    )

    col_img1, col_img2, col_img3 = st.columns(3)
    with col_img1:
        aspect_ratio = st.selectbox("Aspect Ratio", ["1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"], index=0)
    with col_img2:
        image_count = st.number_input("Number of Images", min_value=1, max_value=9, value=1, step=1)
    with col_img3:
        response_format = st.selectbox("Response Format", ["url", "base64"], index=0)

    col_img4, col_img5 = st.columns(2)
    with col_img4:
        seed_value = st.text_input("Seed (optional, integer)", placeholder="Leave blank for random")
    with col_img5:
        prompt_optimizer = st.checkbox("Enable Prompt Optimizer", value=False)

    if st.button("Generate Image", key="btn_image"):
        if not image_prompt:
            st.error("Please enter an image prompt!")
            return

        with st.spinner("Generating image(s)..."):
            url = os.environ.get("MINIMAX_API_URL_IMAGE", "https://api.minimax.io/v1/image_generation")
            payload = {
                "model": "image-01",
                "prompt": image_prompt,
                "aspect_ratio": aspect_ratio,
                "response_format": response_format,
                "n": int(image_count),
                "prompt_optimizer": prompt_optimizer,
            }

            if seed_value.strip():
                try:
                    payload["seed"] = int(seed_value.strip())
                except ValueError:
                    st.error("Seed must be an integer.")
                    return

            try:
                res = requests.post(url, headers=headers, json=payload)
                res.raise_for_status()
                data = res.json()

                if "base_resp" in data and data["base_resp"].get("status_code", 0) != 0:
                    st.error(f"API Error: {data['base_resp'].get('status_msg', 'Unknown error')}")
                    st.json(data)
                    return

                st.success("Image generated successfully!")
                image_data = data.get("data", {}) if isinstance(data, dict) else {}

                if response_format == "url":
                    image_urls = image_data.get("image_urls", [])
                    if image_urls:
                        for idx, img_url in enumerate(image_urls, start=1):
                            st.image(img_url, caption=f"Generated Image {idx}", use_container_width=True)
                    else:
                        st.info("No image URLs found in response.")
                else:
                    image_base64_list = image_data.get("image_base64", [])
                    if image_base64_list:
                        for idx, img_b64 in enumerate(image_base64_list, start=1):
                            st.image(f"data:image/png;base64,{img_b64}", caption=f"Generated Image {idx}", use_container_width=True)
                    else:
                        st.info("No base64 images found in response.")

                with st.expander("Show raw JSON response"):
                    st.json(data)
            except Exception as e:
                st.error(f"Error: {e}")
                if hasattr(e, "response") and e.response is not None:
                    try:
                        st.json(e.response.json())
                    except Exception:
                        st.text(e.response.text)
