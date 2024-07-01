import re
import os
import time
import streamlit as st
import yaml
#from siagpt_functions import generate_answer
from openai_functions import generate_answer
from audio_generation import get_b64_audio
from streamlit_utils import autoplay_audio

#PROJECT_CONFIG = yaml.safe_load(os.getenv("PROJECT_CONFIG"))
#with open("project_config.yml", 'r', encoding='utf-8') as stream:
#    PROJECT_CONFIG = yaml.safe_load(stream)
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
PROJECT_ID = os.getenv("PROJECT_ID")

def speech_to_text(audio_input):
    #Takes audio input and uses whisper api to convert it into text
    return

def generate_response(user_input):
    #Takes text input and uses SiaGPT API to convert it into text
    #response = generate_answer(user_input, ASSISTANT_ID, PROJECT_ID)
    #texte = eval(response)["response"]
    texte = generate_answer(user_input)
    pattern = r'<output>([\s\S]*?)<\/output>'
    match = re.findall(pattern, texte)[0]
    return match

def text_to_speech(siagpt_response, output_path):
    b64_audio = get_b64_audio(siagpt_response, output_path)
    return b64_audio

def main():
    st.title("Elisabeth Moreno Bot")
    with st.form(key='chat_form'):
        user_input = st.text_input("Enter your message", key="input")
        submit_button = st.form_submit_button(label='Send')
    placeholder = st.empty()
    if submit_button:
        placeholder.empty()
        with st.spinner('Processing...'):
            response = generate_response(user_input)
            b64_audio = text_to_speech(response, output_path="ElisabethMorenoBot.mp3")
            time.sleep(2)
        with placeholder.container():
            st.write("Elisabeth Moreno Bot:", response)
            if b64_audio:
                autoplay_audio(b64_audio)

if __name__ == "__main__":
    main()
