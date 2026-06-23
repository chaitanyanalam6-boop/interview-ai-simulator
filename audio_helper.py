import speech_recognition as sr
import os

def speak_text(text):
    # Clean up quotes to prevent terminal syntax issues
    clean_text = text.replace('"', '').replace("'", "")
    
    # We use a natural, clear voice ('Samantha') and set the speech rate to 160 words per minute (normal human speed)
    # If you prefer a male voice, you can change "Samantha" to "Alex"
    os.system(f'say -v "Samantha" -r 160 "{clean_text}"')

def record_and_transcribe():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 AI Recruiter is listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        
    try:
        print("🤖 Transcribing your answer...")
        text = recognizer.recognize_google(audio)
        print(f"You said: \"{text}\"")
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I couldn't understand the audio.")
        return None
    except sr.RequestError:
        print("❌ Speech service down.")
        return None