import os
import re
from audio_helper import record_and_transcribe
from llm_helper import get_interview_feedback, generate_interview_question

def extract_score(evaluation_text):
    match = re.search(r'### Score\s*\n*\[?(\d+)/10\]?', evaluation_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match_fallback = re.search(r'(\d+)\s*/\s*10', evaluation_text)
    if match_fallback:
        return int(match_fallback.group(1))
    return 0

def run_simulator():
    print("=" * 50)
    print("🤖 ADVANCED AI INTERVIEW SIMULATOR 🤖")
    print("=" * 50)
    
    field = input("\n💼 What topic/field would you like to be interviewed on? (e.g., Python, SQL, Machine Learning): ")
    if not field.strip():
        field = "General Software Engineering"
        
    total_questions = 10
    score_history = []
    
    print(f"\n🚀 Starting a {total_questions}-question interview on: {field.upper()}\n")
    
    for q_num in range(1, total_questions + 1):
        print(f"\n--- 📋 Question {q_num} of {total_questions} ---")
            
        # Call our brand new function to get a clean question!
        question = generate_interview_question(field, q_num)
        print(f"\n🤖 Recruiter: {question}")
        
        input("\nPress Enter when you are ready to speak your answer...")
        
        user_answer = record_and_transcribe()
        
        if not user_answer:
            print("No answer detected. Skipping this question with a score of 0.")
            score_history.append(0)
            continue

        print("\n🔄 Analyzing your answer...")
        evaluation = get_interview_feedback(question, user_answer)
        
        print("\n" + "-" * 30)
        print(evaluation)
        print("-" * 30)
        
        score = extract_score(evaluation)
        score_history.append(score)
        print(f"📊 Running Total Score: {sum(score_history)} / {q_num * 10}")

    print("\n" + "=" * 50)
    print("🏆 FINAL INTERVIEW SCORECARD 🏆")
    print("=" * 50)
    final_score = sum(score_history)
    max_possible = total_questions * 10
    percentage = (final_score / max_possible) * 100
    
    print(f"Total Points: {final_score} / {max_possible} ({percentage:.1f}%)")
    
    if percentage >= 80:
        print("Verdict: Excellent job! You are ready for the real interview. 🎉")
    elif percentage >= 50:
        print("Verdict: Good effort! Review the feedback areas to sharpen your answers. 👍")
    else:
        print("Verdict: Keep practicing! Use the critiques above to study up. 💪")
    print("=" * 50)

if __name__ == "__main__":
    run_simulator()