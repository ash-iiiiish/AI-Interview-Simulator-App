import os
import time
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
API_BASE = os.getenv("BACKEND_URL", "http://localhost:8000") + "/api"

st.set_page_config(
    page_title="InterviewAI — Practice Like a Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROUNDS = ["HR", "APTITUDE", "TECHNICAL", "DSA"]
ROUND_META = {
    "HR": {"label": "HR Round", "icon": "👤", "color": "#3b82f6", "accent": "#2563eb"},
    "APTITUDE": {"label": "Aptitude Round", "icon": "🧮", "color": "#f59e0b", "accent": "#d97706"},
    "TECHNICAL": {"label": "Technical Round", "icon": "💻", "color": "#10b981", "accent": "#059669"},
    "DSA": {"label": "DSA Round", "icon": "🔢", "color": "#ef4444", "accent": "#dc2626"},
}

INTERVIEWER_DATA = {
    "HR": {"emoji": "👩‍💼", "name": "Sarah Chen", "title": "HR Business Partner", "company": "TechCorp Inc."},
    "APTITUDE": {"emoji": "🧑‍🏫", "name": "Prof. Arjun", "title": "Assessment Specialist", "company": "EvalPro Solutions"},
    "TECHNICAL": {"emoji": "👨‍💻", "name": "Alex Rivera", "title": "Principal Engineer", "company": "Silicon Labs"},
    "DSA": {"emoji": "🤖", "name": "ARIA-9", "title": "Algorithm Intelligence", "company": "DeepCode AI"},
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.block-container {
    padding: 1rem 2rem 3rem !important;
    max-width: 1400px;
    margin: 0 auto;
}

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #e2e8f0;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb {
    background: #94a3b8;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #64748b;
}

.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.8rem;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 24px;
    margin-bottom: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
.nav-logo {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}
.nav-badge {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 1rem;
    background: #f1f5f9;
    border-radius: 100px;
    font-size: 0.75rem;
    color: #475569;
}
.nav-right {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.8rem;
    color: #64748b;
}

.progress-track {
    display: flex;
    align-items: center;
    background: white;
    border-radius: 60px;
    padding: 0.5rem 1rem;
    margin-bottom: 2rem;
    border: 1px solid #e2e8f0;
}
.prog-step {
    display: flex;
    align-items: center;
    flex: 1;
}
.prog-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
    flex-shrink: 0;
}
.prog-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    background: #f1f5f9;
    border: 2px solid #e2e8f0;
    color: #64748b;
    transition: all 0.3s ease;
}
.prog-circle.done {
    background: #22c55e;
    border-color: #22c55e;
    color: white;
}
.prog-circle.active {
    background: #3b82f6;
    border-color: #3b82f6;
    color: white;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}
.prog-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #64748b;
    white-space: nowrap;
}
.prog-label.active {
    color: #3b82f6;
}
.prog-label.done {
    color: #22c55e;
}
.prog-line {
    flex: 1;
    height: 2px;
    background: #e2e8f0;
    margin: 0 0.5rem;
    margin-bottom: 1.2rem;
    border-radius: 2px;
}
.prog-line.done {
    background: #22c55e;
}

.interviewer-panel {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.panel-header {
    padding: 1rem 1.5rem;
    background: #fafbfc;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.panel-rec {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.7rem;
    font-weight: 600;
    color: #ef4444;
}
.rec-dot {
    width: 8px;
    height: 8px;
    background: #ef4444;
    border-radius: 50%;
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
}
.panel-id {
    font-size: 0.7rem;
    font-family: monospace;
    color: #94a3b8;
}

.avatar-stage {
    padding: 2rem 1.5rem 1rem;
    text-align: center;
}
.avatar-emoji-wrap {
    width: 120px;
    height: 120px;
    margin: 0 auto;
    background: linear-gradient(135deg, #f1f5f9, #ffffff);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3.5rem;
    border: 3px solid #e2e8f0;
    transition: all 0.3s ease;
}
.avatar-emoji-wrap.speaking {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}
.interviewer-name {
    font-size: 1.2rem;
    font-weight: 700;
    margin-top: 1rem;
    color: #0f172a;
}
.interviewer-title {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 0.25rem;
}
.interviewer-company {
    font-size: 0.7rem;
    color: #3b82f6;
    margin-top: 0.5rem;
}

.hud-chips {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    margin: 1rem 0;
}
.hud-chip {
    padding: 0.25rem 0.75rem;
    background: #f1f5f9;
    border-radius: 20px;
    font-size: 0.7rem;
    font-family: monospace;
    color: #475569;
}

.round-tag {
    text-align: center;
    margin: 1rem 0;
}
.round-tag-inner {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 1rem;
    background: #f1f5f9;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
}

.question-bubble {
    margin: 0 1.5rem 1rem;
    padding: 1.2rem;
    background: #f8fafc;
    border-left: 4px solid #3b82f6;
    border-radius: 12px;
    font-family: monospace;
    font-size: 0.9rem;
    line-height: 1.6;
    color: #0f172a;
}
.typing-cursor {
    display: inline-block;
    width: 2px;
    height: 1em;
    background: #3b82f6;
    margin-left: 2px;
    animation: blink 1s step-end infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

.q-counter {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1.5rem 1.5rem;
    font-size: 0.7rem;
    color: #64748b;
}
.q-dots {
    display: flex;
    gap: 0.5rem;
}
.q-dot {
    width: 24px;
    height: 3px;
    background: #e2e8f0;
    border-radius: 2px;
}
.q-dot.done {
    background: #22c55e;
}
.q-dot.active {
    background: #3b82f6;
}

.chat-panel {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 24px;
    padding: 1.5rem;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.panel-title {
    font-size: 0.7rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-title::before {
    content: '';
    width: 3px;
    height: 12px;
    background: linear-gradient(135deg, #3b82f6, #4f46e5);
    border-radius: 2px;
}

.chat-scroll {
    flex: 1;
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 1rem;
}
.msg-row {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1rem;
    animation: slideIn 0.3s ease;
}
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.msg-row.user {
    flex-direction: row-reverse;
}
.msg-ava {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
}
.msg-ava.ai {
    background: #f1f5f9;
}
.msg-ava.you {
    background: #eef2ff;
}
.msg-bubble {
    max-width: 80%;
    padding: 0.75rem 1rem;
    border-radius: 16px;
    font-size: 0.85rem;
    line-height: 1.5;
}
.msg-bubble.ai {
    background: #f1f5f9;
    color: #0f172a;
    border-top-left-radius: 4px;
}
.msg-bubble.you {
    background: #eef2ff;
    color: #1e293b;
    border-top-right-radius: 4px;
}

.stTextArea textarea {
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    color: #0f172a !important;
    font-size: 0.85rem !important;
    padding: 0.75rem !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    outline: none !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #3b82f6, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 40px !important;
    padding: 0.7rem !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

.hero-section {
    text-align: center;
    padding: 3rem 2rem;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.3rem 1rem;
    background: #f1f5f9;
    border-radius: 100px;
    font-size: 0.7rem;
    color: #475569;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.2;
    background: linear-gradient(135deg, #0f172a, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}
.hero-sub {
    font-size: 1rem;
    color: #475569;
    max-width: 600px;
    margin: 0 auto 2rem;
}

.feat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    max-width: 800px;
    margin: 0 auto 2rem;
}
.feat-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    transition: all 0.2s ease;
}
.feat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
.feat-icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}
.feat-name {
    font-size: 0.75rem;
    font-weight: 600;
    color: #3b82f6;
    margin-bottom: 0.25rem;
}
.feat-desc {
    font-size: 0.7rem;
    color: #64748b;
}

.upload-zone {
    background: white;
    border: 2px dashed #cbd5e1;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

def api(method: str, path: str, **kwargs):
    try:
        r = requests.request(method, f"{API_BASE}{path}", timeout=60, **kwargs)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("Cannot reach the backend. Make sure the FastAPI server is running on port 8000.")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def init_state():
    defaults = {
        "page": "landing",
        "session_token": None,
        "resume_data": {},
        "resume_score": {},
        "current_round": "HR",
        "current_question": "",
        "question_number": 0,
        "chat_history": [],
        "rounds_completed": [],
        "last_eval": None,
        "final_report": None,
        "is_speaking": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def render_navbar(show_status: bool = False):
    session_info = ""
    if show_status and st.session_state.session_token:
        rnd = st.session_state.current_round
        meta = ROUND_META.get(rnd, {})
        session_info = f'<div class="nav-badge">{meta.get("icon","🎯")} {meta.get("label","Interview")}</div>'
    
    st.markdown(f"""
    <div class="navbar">
        <div class="nav-logo">INTERVIEW<span style="background:none; -webkit-text-fill-color:#334155;">AI</span></div>
        <div style="display:flex;align-items:center;gap:1rem;">
            {session_info}
            <div class="nav-right">
                <span>Powered by Groq</span>
                <span style="color:#cbd5e1;">|</span>
                <span>llama-3.3-70b</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_progress(current_round: str, rounds_completed: list):
    steps_html = ""
    for i, r in enumerate(ROUNDS):
        is_done = r in rounds_completed
        is_active = r == current_round and r not in rounds_completed
        circle_cls = "active" if is_active else ("done" if is_done else "")
        label_cls = "active" if is_active else ("done" if is_done else "")
        icon = "✓" if is_done else ROUND_META[r]["icon"]
        
        steps_html += f"""
        <div class="prog-step">
            <div class="prog-node">
                <div class="prog-circle {circle_cls}">{icon}</div>
                <div class="prog-label {label_cls}">{ROUND_META[r]['label']}</div>
            </div>
            {"" if i == len(ROUNDS)-1 else f'<div class="prog-line {"done" if i < len(ROUNDS)-1 and (ROUNDS[i+1] in rounds_completed or ROUNDS[i+1] == current_round or is_done) else ""}"></div>'}
        </div>
        """
    st.markdown(f'<div class="progress-track">{steps_html}</div>', unsafe_allow_html=True)

def render_interviewer_panel(round_name: str, question: str, q_num: int, total_q: int = 5):
    meta = ROUND_META.get(round_name, {})
    interviewer = INTERVIEWER_DATA.get(round_name, {})
    speaking_class = "speaking" if st.session_state.is_speaking else ""
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
        <div class="interviewer-panel">
            <div class="panel-header">
                <div class="panel-rec">
                    <div class="rec-dot"></div>
                    <span>LIVE</span>
                </div>
                <div class="panel-id">{meta.get("label", "")}</div>
            </div>
            <div class="avatar-stage">
                <div class="avatar-emoji-wrap {speaking_class}">
                    {interviewer.get("emoji", "🤖")}
                </div>
                <div class="interviewer-name">{interviewer.get("name", "Interviewer")}</div>
                <div class="interviewer-title">{interviewer.get("title", "")}</div>
                <div class="interviewer-company">{interviewer.get("company", "")}</div>
            </div>
            <div class="hud-chips">
                <div class="hud-chip">🎯 {meta.get("label", "")}</div>
                <div class="hud-chip">📋 Q{q_num+1}/{total_q}</div>
            </div>
            <div class="round-tag">
                <div class="round-tag-inner">
                    <span>{meta.get("icon", "")}</span>
                    <span>{meta.get("label", "")}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="interviewer-panel">
            <div class="panel-header">
                <div class="panel-id">Current Question</div>
            </div>
            <div class="question-bubble">
                {question}
                <span class="typing-cursor"></span>
            </div>
            <div class="q-counter">
                <span>Question {q_num+1} of {total_q}</span>
                <div class="q-dots">
        """, unsafe_allow_html=True)
        
        for i in range(total_q):
            if i < q_num:
                st.markdown('<div class="q-dot done"></div>', unsafe_allow_html=True)
            elif i == q_num:
                st.markdown('<div class="q-dot active"></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="q-dot"></div>', unsafe_allow_html=True)
        
        st.markdown(f"""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_chat_panel(chat_history: list):
    st.markdown(f"""
    <div class="chat-panel">
        <div class="panel-title">Conversation Log</div>
        <div class="chat-scroll">
    """, unsafe_allow_html=True)
    
    for msg in chat_history:
        if msg["role"] == "assistant":
            st.markdown(f"""
            <div class="msg-row">
                <div class="msg-ava ai">🤖</div>
                <div class="msg-bubble ai">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row user">
                <div class="msg-ava you">👤</div>
                <div class="msg-bubble you">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""
        </div>
    </div>
    """, unsafe_allow_html=True)

def landing_page():
    render_navbar()
    
    st.markdown("""
    <div class="hero-section">
        <div class="hero-eyebrow">
            <span>✨ AI-Powered Mock Interviews</span>
        </div>
        <div class="hero-title">
            Ace Your Next Interview<br>
            with Confidence
        </div>
        <div class="hero-sub">
            Practice with AI interviewers, get real-time feedback, and track your progress across all interview rounds.
        </div>
        <div class="feat-grid">
            <div class="feat-card">
                <div class="feat-icon">👤</div>
                <div class="feat-name">HR Round</div>
                <div class="feat-desc">Behavioral & cultural fit</div>
            </div>
            <div class="feat-card">
                <div class="feat-icon">🧮</div>
                <div class="feat-name">Aptitude</div>
                <div class="feat-desc">Quant & logical reasoning</div>
            </div>
            <div class="feat-card">
                <div class="feat-icon">💻</div>
                <div class="feat-name">Technical</div>
                <div class="feat-desc">Domain expertise</div>
            </div>
            <div class="feat-card">
                <div class="feat-icon">🔢</div>
                <div class="feat-name">DSA</div>
                <div class="feat-desc">Data structures & algorithms</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"], key="resume_upload")
        
        if uploaded_file:
            files = {"file": ("resume.pdf", uploaded_file.getvalue(), "application/pdf")}
            result = api("POST", "/analyze-resume", files=files)
            
            if result:
                st.session_state.resume_data = result.get("resume_data", {})
                st.session_state.resume_score = result.get("score", {})
                st.session_state.page = "interview"
                st.rerun()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Start Practice Session →", use_container_width=True):
                if not uploaded_file:
                    st.warning("Please upload your resume first")
                else:
                    init_data = api("POST", "/init-session", json={"resume_data": st.session_state.resume_data})
                    if init_data:
                        st.session_state.session_token = init_data.get("session_token")
                        st.session_state.current_round = init_data.get("current_round", "HR")
                        st.session_state.current_question = init_data.get("question", "Tell me about yourself.")
                        st.session_state.chat_history = [{"role": "assistant", "content": st.session_state.current_question}]
                        st.session_state.page = "interview"
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def interview_page():
    render_navbar(show_status=True)
    render_progress(st.session_state.current_round, st.session_state.rounds_completed)
    
    total_q = 5
    render_interviewer_panel(
        st.session_state.current_round,
        st.session_state.current_question,
        st.session_state.question_number,
        total_q
    )
    
    col_chat, col_input = st.columns([2, 1])
    
    with col_chat:
        render_chat_panel(st.session_state.chat_history)
    
    with col_input:
        st.markdown('<div class="chat-panel" style="padding: 1rem;">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Your Answer</div>', unsafe_allow_html=True)
        
        answer = st.text_area("Type your response here...", height=200, key="answer_input", label_visibility="collapsed")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit = st.button("Submit Answer", use_container_width=True)
        with col_btn2:
            if st.button("End Session", use_container_width=True):
                report = api("POST", "/final-report", json={"session_token": st.session_state.session_token})
                if report:
                    st.session_state.final_report = report
                    st.session_state.page = "results"
                    st.rerun()
        
        if submit and answer:
            st.session_state.chat_history.append({"role": "user", "content": answer})
            st.session_state.is_speaking = True
            
            eval_response = api("POST", "/evaluate", json={
                "session_token": st.session_state.session_token,
                "answer": answer,
                "round_name": st.session_state.current_round
            })
            
            if eval_response:
                st.session_state.last_eval = eval_response
                score = eval_response.get("score", 0)
                feedback = eval_response.get("feedback", "")
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"📊 Score: {score}/10\n\n💡 Feedback: {feedback}"
                })
                
                if eval_response.get("move_next", False):
                    next_q = api("POST", "/next-question", json={"session_token": st.session_state.session_token})
                    if next_q:
                        if next_q.get("round_completed", False):
                            st.session_state.rounds_completed.append(st.session_state.current_round)
                            next_round_idx = ROUNDS.index(st.session_state.current_round) + 1
                            if next_round_idx < len(ROUNDS):
                                st.session_state.current_round = ROUNDS[next_round_idx]
                                st.session_state.question_number = 0
                                st.session_state.current_question = next_q.get("question", "")
                                st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.current_question})
                            else:
                                report = api("POST", "/final-report", json={"session_token": st.session_state.session_token})
                                if report:
                                    st.session_state.final_report = report
                                    st.session_state.page = "results"
                        else:
                            st.session_state.current_question = next_q.get("question", "")
                            st.session_state.question_number += 1
                            st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.current_question})
            
            st.session_state.is_speaking = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def results_page():
    render_navbar()
    
    report = st.session_state.final_report
    if not report:
        st.error("No report available")
        if st.button("Start New Session"):
            st.session_state.page = "landing"
            st.rerun()
        return
    
    overall_score = report.get("overall_score", 0)
    grade = report.get("grade", "C")
    verdict = report.get("verdict", "Consider")
    summary = report.get("summary", "")
    
    verdict_class = "v-hire" if "hire" in verdict.lower() else ("v-maybe" if "consider" in verdict.lower() else "v-no")
    verdict_text = "🎉 RECOMMENDED FOR HIRE" if "hire" in verdict.lower() else ("📝 CONSIDER FOR NEXT ROUND" if "consider" in verdict.lower() else "📋 NEEDS IMPROVEMENT")
    
    st.markdown(f"""
    <div class="report-banner">
        <div class="verdict-chip {verdict_class}">{verdict_text}</div>
        <div class="final-score">{overall_score}<span style="font-size:1.5rem;">/100</span></div>
        <div class="grade-tag">Grade {grade}</div>
        <div class="exec-summary">{summary}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="info-card"><div class="info-card-title">Round-wise Performance</div>', unsafe_allow_html=True)
        round_scores = report.get("round_scores", {})
        for round_name in ROUNDS:
            score = round_scores.get(round_name, 0)
            percentage = (score / 10) * 100 if score <= 10 else score
            st.markdown(f"""
            <div style="margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:0.25rem;">
                    <span>{ROUND_META[round_name]["icon"]} {ROUND_META[round_name]["label"]}</span>
                    <span><strong>{score}/10</strong></span>
                </div>
                <div class="bar-track">
                    <div class="bar-fill" style="width:{percentage}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card"><div class="info-card-title">Key Strengths</div>', unsafe_allow_html=True)
        for strength in report.get("strengths", ["Communication Skills", "Technical Knowledge", "Problem Solving"])[:3]:
            st.markdown(f'<div class="check-row">✅ {strength}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-card-title" style="margin-top:1rem;">Areas for Improvement</div>', unsafe_allow_html=True)
        for improvement in report.get("improvements", ["Practice more", "Structure answers better", "Time management"])[:3]:
            st.markdown(f'<div class="check-row">🎯 {improvement}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Start New Practice Session", use_container_width=True):
        for key in ["session_token", "resume_data", "resume_score", "current_round", "current_question", 
                    "question_number", "chat_history", "rounds_completed", "last_eval", "final_report"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.page = "landing"
        st.rerun()

if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "interview":
    interview_page()
elif st.session_state.page == "results":
    results_page()