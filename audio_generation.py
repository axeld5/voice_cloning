import base64
import os
import requests
import yaml

from pydub import AudioSegment

PROJECT_CONFIG = yaml.safe_load(os.getenv("PROJECT_CONFIG"))
#with open("project_config.yml", 'r', encoding='utf-8') as stream:
#    PROJECT_CONFIG = yaml.safe_load(stream)
CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
XI_API_KEY = PROJECT_CONFIG["XI_API_KEY"]  # Your API key for authentication
ELISABOT_VOICE_ID = PROJECT_CONFIG["ELISABOT_VOICE_ID"]  # ID of the voice model to use

def save_audio_file(siagpt_response, output_path):
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELISABOT_VOICE_ID}/stream"
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }
    data = {
        "text": siagpt_response,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    response = requests.post(tts_url, headers=headers, json=data, stream=True, timeout=30000)
    if response.ok:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        print("Audio stream saved successfully.")
    else:
        print(response.text)

def change_audio_speed(input_file, output_file, speed=1.0):
    audio = AudioSegment.from_file(input_file)
    new_audio = audio._spawn(audio.raw_data, overrides={
         "frame_rate": int(audio.frame_rate * speed)
      }).set_frame_rate(audio.frame_rate)
    new_audio.export(output_file, format="mp3")

def get_b64_audio(siagpt_response, output_path):
    save_audio_file(siagpt_response, output_path)
    #change_audio_speed(output_path, output_path, 0.95)
    with open(output_path, 'rb') as file:
        audio_data = file.read()
        b64_audio = base64.b64encode(audio_data).decode()
    return b64_audio
