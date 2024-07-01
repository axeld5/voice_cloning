import streamlit as st

def autoplay_audio(b64_audio):
    #Takes b64 audio version of a file and creates audio component with autoplay
    md = f"""
            <style>
            .audio-container {{
                width: 100%;
                max-width: 700px; /* Adjust this as needed */
            }}
            </style>
            <div class="audio-container">
            <audio controls autoplay="true" style="width: 100%;">
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            </audio>
    """
    st.markdown(
        md,
        unsafe_allow_html=True,
    )