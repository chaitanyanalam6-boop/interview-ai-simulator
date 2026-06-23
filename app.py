from audio_helper import process_browser_audio, speak_text

col_a, col_b = st.columns([1, 2])
    with col_a:
        if st.button("🔊 Read question aloud", use_container_width=True):
            speak_text(st.session_state.active_question)
            
    with col_b:
        st.markdown(" ") # just for alignment
        
    # --- NEW WEB MICROPHONE WIDGET ---
    st.markdown("<br>", unsafe_allow_html=True)
    audio_bytes = st.audio_input("Record your answer below", disabled=st.session_state.answered)

    if audio_bytes and not st.session_state.answered:
        with st.spinner("Scoring your answer…"):
            # Process the browser's audio file stream directly
            user_answer = process_browser_audio(audio_bytes)
            
            if user_answer:
                st.session_state.last_answer = user_answer
                evaluation = get_interview_feedback(st.session_state.active_question, user_answer)
                st.session_state.last_evaluation = evaluation
                st.session_state.score_history.append(extract_score(evaluation))
                st.session_state.answered = True
                st.rerun()
            else:
                st.error("Could not decode audio transcription data. Please try speaking closer to your mic.")