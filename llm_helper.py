import streamlit as st
from groq import Groq

# 1. Check if the secret key name exists at all in your Streamlit settings
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ CRITICAL: Streamlit Cloud cannot find a secret named 'GROQ_API_KEY'. Please open your Secrets Dashboard and check the spelling.")
    st.stop()

# 2. Extract the key value safely
api_key_value = st.secrets["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"]

# 3. Check if the key value was accidentally left blank or contains placeholders
if not api_key_value or api_key_value.strip() == "" or "your_actual_key" in api_key_value:
    st.error("❌ CRITICAL: The GROQ_API_KEY secret exists in your dashboard, but it is empty or contains placeholder text.")
    st.stop()

# 4. Initialize the Groq client securely using the validated key string
try:
    client = Groq(api_key=api_key_value)
except Exception as e:
    st.error(f"❌ CRITICAL: Failed to initialize Groq client: {str(e)}")
    st.stop()


def generate_interview_question(field, question_number):
    """
    Generates a structured interview question based on the chosen career field.
    """
    messages = [
        {
            "role": "system",
            "content": (
                f"You are an expert technical interviewer in the field of {field}. "
                f"Ask a precise, realistic interview question suited for a junior to mid-level role. "
                "Output ONLY the question text. Do not include introductory text, conversational pleasantries, "
                "or conversational follow-ups."
            )
        },
        {
            "role": "user",
            "content": f"Generate interview question number {question_number}."
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"⚠️ Failed to communicate with Groq API: {str(e)}")
        return "Could not generate question due to an unexpected API error."