import streamlit as st
from audio_helper import process_browser_audio, speak_text
from llm_helper import get_interview_feedback, generate_interview_question
import re

def extract_score(evaluation_text):
    match = re.search(r'### Score\s*\n*\[?(\d+)/10\]?', evaluation_text, re.IGNORECASE)
    if match: return int(match.group(1))
    match_fallback = re.search(r'(\d+)\s*/\s*10', evaluation_text)
    if match_fallback: return int(match_fallback.group(1))
    return 0

st.set_page_config(page_title="IntervAI", page_icon="👔", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
.stApp { background: #ffffff; font-family: 'Inter', sans-serif; color: #0f172a; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }

.nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 64px; height: 64px; border-bottom: 1px solid #e2e8f0;
    background: #fff; position: sticky; top: 0; z-index: 100;
}
.nav-logo { font-size: 1.25rem; font-weight: 800; letter-spacing: -0.5px; color: #0f172a; }
.nav-links { display: flex; gap: 32px; }
.nav-links a { color: #475569; font-size: 0.9rem; font-weight: 500; text-decoration: none; }

.hero {
    padding: 96px 64px 80px; max-width: 1200px; margin: 0 auto;
    display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center;
}
.hero-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: #f0fdf4; border: 1px solid #bbf7d0; color: #15803d;
    font-size: 0.78rem; font-weight: 600; padding: 4px 12px; border-radius: 20px;
    text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 24px;
}
.hero-pill .dot { width: 6px; height: 6px; border-radius: 50%; background: #22c55e; display:inline-block; }
.hero h1 { font-size: 3.5rem; font-weight: 800; line-height: 1.1; letter-spacing: -2px; color: #0f172a; margin-bottom: 20px; }
.hero h1 span { color: #6366f1; }
.hero p { font-size: 1.1rem; color: #64748b; line-height: 1.7; margin-bottom: 36px; max-width: 480px; }
.hero-stats { display: flex; gap: 32px; margin-top: 48px; padding-top: 32px; border-top: 1px solid #e2e8f0; }
.stat-num { font-size: 1.75rem; font-weight: 800; color: #0f172a; letter-spacing: -1px; }
.stat-label { font-size: 0.82rem; color: #94a3b8; font-weight: 500; margin-top: 2px; }

.hero-visual { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 20px; padding: 28px; }
.mock-header { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
.mock-avatar {
    width: 36px; height: 36px; border-radius: 50%; background: #6366f1; color: #fff;
    display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 700;
}
.mock-name { font-size: 0.9rem; font-weight: 600; }
.mock-role { font-size: 0.78rem; color: #94a3b8; }
.mock-bubble { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 18px; margin-bottom: 12px; font-size: 0.88rem; line-height: 1.6; color: #374151; }
.mock-bubble.ai { border-left: 3px solid #6366f1; }
.mock-bubble.user { background: #f0f9ff; border-left: 3px solid #0ea5e9; }
.mock-score { display: flex; align-items: center; justify-content: space-between; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 12px 16px; margin-top: 8px; }
.score-val { font-size: 1.5rem; font-weight: 800; color: #15803d; }
.score-bar { height: 6px; background: #e2e8f0; border-radius: 3px; margin-top: 6px; overflow: hidden; }
.score-fill { height: 100%; background: #22c55e; border-radius: 3px; width: 78%; }

.features { background: #f8fafc; padding: 96px 64px; border-top: 1px solid #e2e8f0; }
.section-label { font-size: 0.78rem; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: #6366f1; margin-bottom: 12px; }
.section-title { font-size: 2.5rem; font-weight: 800; letter-spacing: -1.5px; color: #0f172a; margin-bottom: 14px; max-width: 600px; }
.section-sub { font-size: 1.05rem; color: #64748b; max-width: 540px; margin-bottom: 56px; }
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; max-width: 1200px; margin: 0 auto; }
.feature-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 28px; }
.feature-icon { width: 44px; height: 44px; border-radius: 10px; background: #ede9fe; color: #6366f1; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; margin-bottom: 16px; }
.feature-card h3 { font-size: 1rem; font-weight: 700; margin-bottom: 8px; color: #0f172a; }
.feature-card p { font-size: 0.88rem; color: #64748b; line-height: 1.6; }

.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; margin-top: 56px; }
.step { padding: 0 32px; }
.step:not(:last-child) { border-right: 1px solid #e2e8f0; }
.step-num { font-size: 3rem; font-weight: 800; color: #e2e8f0; letter-spacing: -2px; margin-bottom: 16px; line-height: 1; }
.step h3 { font-size: 1.05rem; font-weight: 700; margin-bottom: 8px; color: #0f172a; }
.step p { font-size: 0.88rem; color: #64748b; line-height: 1.6; }

.interview-section { padding: 96px 64px; background: #f8fafc; border-top: 1px solid #e2e8f0; }
.i-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 40px; margin-bottom: 20px; }
.q-box { background: #f0f9ff; border-left: 4px solid #6366f1; border-radius: 0 12px 12px 0; padding: 20px 24px; font-size: 1.05rem; color: #1e293b; line-height: 1.6; margin: 20px 0; }
.fb-box { background: #f0fdf4; border-left: 4px solid #22c55e; border-radius: 0 12px 12px 0; padding: 16px 20px; font-size: 0.93rem; color: #14532d; margin-top: 16px; }
.progress-wrap { margin-bottom: 24px; }
.progress-label { display: flex; justify-content: space-between; font-size: 0.82rem; color: #64748b; margin-bottom: 8px; }
.progress-track { height: 6px; background: #e2e8f0; border-radius: 3px; overflow: hidden; }

.footer { padding: 40px 64px; border-top: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; background: #fff; }
.footer-logo { font-size: 1rem; font-weight: 800; color: #0f172a; }
.footer-note { font-size: 0.82rem; color: #94a3b8; }

div.stTextInput > div > div > input {
    border-radius: 10px !important; border: 1.5px solid #e2e8f0 !important;
    padding: 14px 16px !important; font-size: 1rem !important;
    font-family: 'Inter', sans-serif !important; background: #fff !important; color: #0f172a !important;
}
div.stButton > button { border-radius: 10px !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important; font-size: 1rem !important; padding: 12px 24px !important; }
</style>
""", unsafe_allow_html=True)

defaults = {
    "stage": "home", "field": "", "current_q": 1, "score_history": [],
    "active_question": "", "interviewer_tone": "Warm & Encouraging",
    "max_questions": 5, "last_evaluation": "", "last_answer": "", "answered": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── LANDING PAGE ─────────────────────────────────────────────────────────────
if st.session_state.stage == "home":

    st.markdown("""
    <nav class="nav">
        <span class="nav-logo">👔 IntervAI</span>
        <div class="nav-links">
            <a href="#features">Features</a>
            <a href="#how">How it works</a>
            <a href="#practice">Practice now</a>
        </div>
    </nav>""", unsafe_allow_html=True)

    st.markdown("""
    <section class="hero">
        <div>
            <div class="hero-pill"><span class="dot"></span> AI-Powered Mock Interviews</div>
            <h1>Ace your next <span>interview</span> with AI feedback</h1>
            <p>Practice real interview questions for any role. Speak your answers, get instant scores and coaching — available 24/7.</p>
            <p style="font-size:0.9rem; color:#94a3b8; margin-bottom:0;">↓ Start practicing below — it's free</p>
            <div class="hero-stats">
                <div><div class="stat-num">10,000+</div><div class="stat-label">Questions available</div></div>
                <div><div class="stat-num">98%</div><div class="stat-label">Say it helped them prepare</div></div>
                <div><div class="stat-num">Any role</div><div class="stat-label">Dev, PM, Design & more</div></div>
            </div>
        </div>
        <div class="hero-visual">
            <div class="mock-header">
                <div class="mock-avatar">AI</div>
                <div>
                    <div class="mock-name">IntervAI Coach</div>
                    <div class="mock-role">Technical Interviewer · Active</div>
                </div>
            </div>
            <div class="mock-bubble ai">Tell me about a time you had to debug a complex production issue. Walk me through your process.</div>
            <div class="mock-bubble user">Sure — last quarter we had a memory leak in our Node service. I isolated it using heap snapshots and traced it back to an event listener that wasn't being cleaned up...</div>
            <div class="mock-score">
                <div><div style="font-size:0.78rem; color:#15803d; font-weight:600;">Score</div><div class="score-val">8 / 10</div></div>
                <div style="flex:1; margin-left:20px;">
                    <div style="font-size:0.78rem; color:#64748b; margin-bottom:4px;">Strong structure. Add quantified impact.</div>
                    <div class="score-bar"><div class="score-fill"></div></div>
                </div>
            </div>
        </div>
    </section>""", unsafe_allow_html=True)

    st.markdown("""
    <section class="features" id="features">
        <div style="max-width:1200px; margin:0 auto;">
            <div class="section-label">Features</div>
            <div class="section-title">Everything you need to prepare</div>
            <div class="section-sub">IntervAI listens, scores, and coaches — so you walk into every interview ready.</div>
            <div class="features-grid">
                <div class="feature-card"><div class="feature-icon">🎙️</div><h3>Voice answers</h3><p>Speak naturally like a real interview. Your answer is transcribed and scored instantly.</p></div>
                <div class="feature-card"><div class="feature-icon">🤖</div><h3>AI-tailored questions</h3><p>Questions generated specifically for your target role — not generic lists.</p></div>
                <div class="feature-card"><div class="feature-icon">📊</div><h3>Instant scoring</h3><p>Get a 1–10 score with detailed feedback on how to improve each answer.</p></div>
                <div class="feature-card"><div class="feature-icon">🎯</div><h3>Any role or industry</h3><p>Software engineer, data analyst, product manager — just tell us the role.</p></div>
                <div class="feature-card"><div class="feature-icon">🔊</div><h3>Audio playback</h3><p>Questions can be read aloud to simulate a real phone or video interview.</p></div>
                <div class="feature-card"><div class="feature-icon">📈</div><h3>Session summary</h3><p>See your total score and performance breakdown at the end of every session.</p></div>
            </div>
        </div>
    </section>""", unsafe_allow_html=True)

    st.markdown("""
    <section style="padding:96px 64px; border-top:1px solid #e2e8f0;" id="how">
        <div style="max-width:1200px; margin:0 auto;">
            <div class="section-label">How it works</div>
            <div class="section-title">Three steps to interview-ready</div>
            <div class="steps">
                <div class="step"><div class="step-num">01</div><h3>Enter your target role</h3><p>Tell us the job title you're going for. IntervAI generates relevant questions on the spot.</p></div>
                <div class="step"><div class="step-num">02</div><h3>Answer out loud</h3><p>Hit record and speak your answer naturally. The AI transcribes it in real time.</p></div>
                <div class="step"><div class="step-num">03</div><h3>Get your score & feedback</h3><p>Receive a detailed score and coaching tips instantly so you can improve each round.</p></div>
            </div>
        </div>
    </section>""", unsafe_allow_html=True)

    st.markdown("""
    <div id="practice" style="background:#f8fafc; border-top:1px solid #e2e8f0;
         padding:72px 64px 24px; text-align:center;">
        <div class="section-label">Start Practicing</div>
        <div style="font-size:2rem; font-weight:800; letter-spacing:-1px;
             color:#0f172a; margin-bottom:10px;">
            Ready? Let's run your mock interview
        </div>
        <p style="color:#64748b; font-size:1rem;">
            It only takes 10 minutes. Enter your role below and hit Start.
        </p>
    </div>""", unsafe_allow_html=True)

    _, col_c, _ = st.columns([1, 2, 1])
    with col_c:
        with st.container(border=True):
            st.markdown("**What role are you interviewing for?**")
            field_input = st.text_input("role", label_visibility="collapsed",
                placeholder="e.g. Python Developer, Data Analyst, Product Manager")

            st.markdown("**Interviewer style**")
            tone = st.selectbox("tone",
                ["Warm & Encouraging", "Professional & Direct", "Strict Technical Drill"],
                label_visibility="collapsed")

            st.markdown("**Number of questions**")
            n_questions = st.slider("nq", 1, 10, 5, label_visibility="collapsed")

            st.markdown(" ")
            if st.button("Start my interview →", type="primary", use_container_width=True):
                if field_input.strip():
                    st.session_state.field            = field_input
                    st.session_state.interviewer_tone = tone
                    st.session_state.max_questions    = n_questions
                    st.session_state.stage            = "interviewing"
                    st.session_state.active_question  = generate_interview_question(field_input, 1)
                    st.session_state.answered         = False
                    st.rerun()
                else:
                    st.error("Please enter a role before starting.")

    st.markdown("""
    <footer class="footer" style="margin-top: 80px;">
        <span class="footer-logo">👔 IntervAI</span>
        <span class="footer-note">Built with Python & Streamlit · AI-powered coaching</span>
    </footer>""", unsafe_allow_html=True)


# ── INTERVIEW PAGE ────────────────────────────────────────────────────────────
elif st.session_state.stage == "interviewing":

    st.markdown('<nav class="nav"><span class="nav-logo">👔 IntervAI</span></nav>', unsafe_allow_html=True)
    st.markdown('<div style="max-width:760px; margin:48px auto; padding:0 24px;">', unsafe_allow_html=True)

    pct = int((st.session_state.current_q - 1) / st.session_state.max_questions * 100)
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-label">
            <span>Question {st.session_state.current_q} of {st.session_state.max_questions} · {st.session_state.field}</span>
            <span>{pct}% complete</span>
        </div>
        <div class="progress-track">
            <div style="height:6px; background:#6366f1; width:{pct}%; border-radius:3px;"></div>
        </div>
    </div>
    <div class="i-card">
        <p style="font-size:0.78rem; font-weight:700; color:#6366f1; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">Question {st.session_state.current_q}</p>
        <div class="q-box">{st.session_state.active_question}</div>
    </div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 2])
    with col_a:
        if st.button("🔊 Read question aloud", use_container_width=True):
            speak_text(st.session_state.active_question)
    with col_b:
        st.markdown(" ")

    st.markdown("<br>", unsafe_allow_html=True)
    audio_bytes = st.audio_input("Record your answer below", disabled=st.session_state.answered)

    if audio_bytes and not st.session_state.answered:
        with st.spinner("Scoring your answer…"):
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

    if st.session_state.answered:
        st.markdown(f"""
        <div class="i-card" style="margin-top:20px;">
            <p style="font-size:0.78rem; font-weight:700; color:#0ea5e9; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">Your answer</p>
            <div style="background:#f0f9ff; border-left:4px solid #0ea5e9; border-radius:0 12px 12px 0; padding:16px 20px; color:#0c4a6e;">"{st.session_state.last_answer}"</div>
        </div>
        <div class="i-card">
            <p style="font-size:0.78rem; font-weight:700; color:#22c55e; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">Feedback & Score</p>
        </div>""", unsafe_allow_html=True)
        st.write(st.session_state.last_evaluation)

        label = "See final results →" if st.session_state.current_q >= st.session_state.max_questions else f"Next question ({st.session_state.current_q + 1}/{st.session_state.max_questions}) →"
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(label, type="primary", use_container_width=True):
            if st.session_state.current_q < st.session_state.max_questions:
                st.session_state.current_q += 1
                st.session_state.active_question = generate_interview_question(st.session_state.field, st.session_state.current_q)
                st.session_state.answered = False
                st.session_state.last_evaluation = ""
                st.session_state.last_answer = ""
                st.rerun()
            else:
                st.session_state.stage = "complete"
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ── RESULTS PAGE ──────────────────────────────────────────────────────────────
elif st.session_state.stage == "complete":
    st.balloons()
    st.markdown('<nav class="nav"><span class="nav-logo">👔 IntervAI</span></nav>', unsafe_allow_html=True)

    final_score  = sum(st.session_state.score_history)
    max_possible = len(st.session_state.score_history) * 10
    percentage   = (final_score / max_possible * 100) if max_possible else 0
    emoji = '🏆' if percentage >= 80 else '📈' if percentage >= 50 else '💪'
    color = '#22c55e' if percentage >= 80 else '#f59e0b' if percentage >= 50 else '#ef4444'

    st.markdown(f"""
    <div style="max-width:760px; margin:64px auto; padding:0 24px; text-align:center;">
        <div style="font-size:3.5rem; margin-bottom:16px;">{emoji}</div>
        <h1 style="font-size:2.5rem; font-weight:800; letter-spacing:-1.5px; margin-bottom:12px;">Interview complete</h1>
        <p style="color:#64748b; font-size:1.05rem; margin-bottom:48px;">
            Here's how you did across {len(st.session_state.score_history)} questions for <strong>{st.session_state.field}</strong>.
        </p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:32px;">
            <div class="i-card" style="text-align:center;">
                <div style="font-size:0.8rem; color:#64748b; font-weight:600; margin-bottom:8px;">TOTAL SCORE</div>
                <div style="font-size:3rem; font-weight:800; color:#0f172a; letter-spacing:-2px;">{final_score}<span style="font-size:1.5rem; color:#94a3b8;">/{max_possible}</span></div>
            </div>
            <div class="i-card" style="text-align:center;">
                <div style="font-size:0.8rem; color:#64748b; font-weight:600; margin-bottom:8px;">ACCURACY</div>
                <div style="font-size:3rem; font-weight:800; color:{color}; letter-spacing:-2px;">{percentage:.0f}<span style="font-size:1.5rem;">%</span></div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    _, col_c, _ = st.columns([1, 3, 1])
    with col_c:
        if percentage >= 80:
            st.success("You're interview-ready! Great structure and confident delivery.")
        elif percentage >= 50:
            st.warning("Good effort! Review the feedback from each question and practice weaker areas.")
        else:
            st.error("Keep practising — try structuring answers using the STAR method.")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Practice again", type="primary", use_container_width=True):
            for k, v in defaults.items(): st.session_state[k] = v
            st.rerun()
        if st.button("← Back to home", use_container_width=True):
            for k, v in defaults.items(): st.session_state[k] = v
            st.session_state.stage = "home"
            st.rerun()