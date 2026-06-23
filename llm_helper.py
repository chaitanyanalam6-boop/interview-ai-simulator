import os
from groq import Groq

# Initialize the free Groq client
client = Groq(api_key="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")

# TOOL 1: Generates questions with a conversational, human style
def generate_interview_question(field, question_number):
    messages = [
        {
            "role": "system", 
            "content": """You are a warm, professional tech recruiter conducting a live voice interview. 
            You speak naturally, directly, and encouragingly. 
            CRITICAL: Output ONLY the question text itself as if you are saying it out loud to the candidate. 
            Never include any introductory phrases like 'Sure, here is your question' or any score layouts."""
        },
        {
            "role": "user", 
            "content": f"Ask me question number {question_number} for a {field} position. Make it sound like a real, conversational interview question."
        }
    ]
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# TOOL 2: Grades your answer like an empathetic, constructive mentor
def get_interview_feedback(question, answer):
    prompt = f"""
    You are an encouraging technical interviewer. Review the candidate's response to the question with empathy and constructive insight.
    
    Interview Question: {question}
    Candidate's Answer: {answer}
    
    Structure your response exactly like this:
    ### Recruiter Feedback
    [Provide a supportive critique. Start by highlighting what they did right or tried to do, followed by a professional, clear explanation of how they can improve or what they might have missed.]
    
    ### Score
    [X/10]
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
