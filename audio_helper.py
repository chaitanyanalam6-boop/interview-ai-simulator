import speech_recognition as sr
from gtts import gTTS
import io
import streamlit as st

def speak_text(text):
    # Generates a clear human voice file using Google TTS
    tts = gTTS(text=text, lang='en', tld='com')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    # Automatically embeds an invisible audio player that plays to the user's browser
    st.audio(fp, format="audio/mp3", autoplay=True)

def process_browser_audio(audio_file):
    recognizer = sr.Recognizer()
    try:
        # Convert the file uploaded by the web browser into an audio structure Python understands
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        st.error(f"Transcription error: {str(e)}")
        return None