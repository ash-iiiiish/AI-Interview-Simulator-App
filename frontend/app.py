"""
AI Interview Simulator — Streamlit Frontend
Avatar-style interviewer UI with rich CSS, animated states, and round progress.
BACKEND_URL is read from .env via load_dotenv.
"""

import os
import time
import requests
import json
import plotly.graph_objects as go
from dotenv import load_dotenv
import streamlit as st

# ── Load .env ──────────────────────────────────────────────────────────────────
load_dotenv()
API_BASE = os.getenv("BACKEND_URL", "http://localhost:8000") + "/api"

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Interview Simulator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Round metadata ─────────────────────────────────────────────────────────────
ROUNDS = ["HR", "APTITUDE", "TECHNICAL", "DSA"]
ROUND_META = {
    "HR":        {"label": "HR Round",        "icon": "👤", "color": "#818cf8", "glow": "rgba(129,140,248,0.35)"},
    "APTITUDE":  {"label": "Aptitude Round",  "icon": "🧮", "color": "#fbbf24", "glow": "rgba(251,191,36,0.35)"},
    "TECHNICAL": {"label": "Technical Round", "icon": "💻", "color": "#34d399", "glow": "rgba(52,211,153,0.35)"},
    "DSA":       {"label": "DSA Round",       "icon": "🔢", "color": "#f87171", "glow": "rgba(248,113,113,0.35)"},
}

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] { font-family: 'Syne', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: #07080f;
    color: #e2e8f0;
}
.block-container {
    padding: 1.5rem 2.5rem !important;
    max-width: 1300px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0d0e1a; }
::-webkit-scrollbar-thumb { background: #2d2f4a; border-radius: 10px; }

/* ────────────────────────────────────────────────
   HEADER
──────────────────────────────────────────────── */
.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2rem 2rem;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    margin-bottom: 2rem;
    backdrop-filter: blur(20px);
}
.app-logo {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #a78bfa, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.app-tagline {
    font-size: 0.78rem;
    color: #475569;
    font-weight: 400;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ────────────────────────────────────────────────
   ROUND PROGRESS BAR
──────────────────────────────────────────────── */
.round-progress {
    display: flex;
    align-items: center;
    gap: 0;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
}
.round-step {
    display: flex;
    align-items: center;
    flex: 1;
}
.round-dot {
    width: 38px; height: 38px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    font-weight: 700;
    border: 2px solid #1e2030;
    background: #0d0e1a;
    color: #3d4060;
    transition: all 0.4s ease;
    flex-shrink: 0;
    position: relative;
}
.round-dot.done {
    background: #1a1f3a;
    border-color: #4f46e5;
    color: #818cf8;
}
.round-dot.active {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    border-color: #818cf8;
    color: white;
    box-shadow: 0 0 20px rgba(129,140,248,0.5);
    animation: pulseDot 2s ease-in-out infinite;
}
@keyframes pulseDot {
    0%, 100% { box-shadow: 0 0 20px rgba(129,140,248,0.5); }
    50%       { box-shadow: 0 0 35px rgba(129,140,248,0.85); }
}
.round-connector {
    flex: 1;
    height: 2px;
    background: #1e2030;
    margin: 0 0.5rem;
    border-radius: 4px;
    transition: background 0.4s ease;
}
.round-connector.done { background: linear-gradient(90deg, #4f46e5, #7c3aed); }
.round-label {
    font-size: 0.62rem;
    text-align: center;
    color: #3d4060;
    margin-top: 0.35rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.round-label.active { color: #818cf8; }
.round-label.done   { color: #6366f1; }

/* ────────────────────────────────────────────────
   AVATAR INTERVIEWER CARD
──────────────────────────────────────────────── */
.avatar-card {
    background: linear-gradient(145deg, #0d0f1e 0%, #111428 60%, #0a0d1a 100%);
    border: 1px solid rgba(129,140,248,0.15);
    border-radius: 24px;
    padding: 2rem 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    overflow: hidden;
}
.avatar-card::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
    pointer-events: none;
}
/* Avatar face */
.avatar-face {
    width: 110px; height: 110px;
    border-radius: 50%;
    background: linear-gradient(145deg, #1e213a, #252844);
    border: 3px solid rgba(129,140,248,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 3rem;
    position: relative;
    margin-bottom: 0.8rem;
    box-shadow: 0 0 40px rgba(99,102,241,0.2), inset 0 2px 4px rgba(255,255,255,0.05);
    animation: avatarFloat 4s ease-in-out infinite;
}
@keyframes avatarFloat {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
}
.avatar-face.speaking {
    border-color: rgba(129,140,248,0.7);
    box-shadow: 0 0 50px rgba(99,102,241,0.45), inset 0 2px 4px rgba(255,255,255,0.05);
    animation: avatarFloat 4s ease-in-out infinite, speakingPulse 1.2s ease-in-out infinite;
}
@keyframes speakingPulse {
    0%, 100% { box-shadow: 0 0 40px rgba(99,102,241,0.35); }
    50%       { box-shadow: 0 0 70px rgba(129,140,248,0.7); }
}
/* Sound wave bars */
.sound-wave {
    display: flex;
    align-items: center;
    gap: 3px;
    height: 28px;
    margin: 0.5rem 0 1rem;
}
.wave-bar {
    width: 3px;
    background: linear-gradient(180deg, #818cf8, #4f46e5);
    border-radius: 3px;
    opacity: 0.3;
}
.wave-bar.active { opacity: 1; }
.wave-bar.active:nth-child(1) { animation: wave 1.1s ease-in-out 0.0s infinite; }
.wave-bar.active:nth-child(2) { animation: wave 1.1s ease-in-out 0.1s infinite; }
.wave-bar.active:nth-child(3) { animation: wave 1.1s ease-in-out 0.2s infinite; }
.wave-bar.active:nth-child(4) { animation: wave 1.1s ease-in-out 0.3s infinite; }
.wave-bar.active:nth-child(5) { animation: wave 1.1s ease-in-out 0.2s infinite; }
.wave-bar.active:nth-child(6) { animation: wave 1.1s ease-in-out 0.1s infinite; }
.wave-bar.active:nth-child(7) { animation: wave 1.1s ease-in-out 0.0s infinite; }
@keyframes wave {
    0%, 100% { height: 4px; }
    50%       { height: 22px; }
}
.avatar-name {
    font-size: 1.05rem;
    font-weight: 700;
    color: #c7d2fe;
    margin-bottom: 0.2rem;
}
.avatar-title {
    font-size: 0.7rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 1.5rem;
}
/* Interviewer speech bubble */
.speech-bubble {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(129,140,248,0.15);
    border-radius: 16px;
    border-top-left-radius: 4px;
    padding: 1.2rem 1.4rem;
    font-size: 0.92rem;
    line-height: 1.7;
    color: #cbd5e1;
    width: 100%;
    position: relative;
    font-family: 'DM Mono', monospace !important;
    font-weight: 300;
}
.speech-bubble::before {
    content: '';
    position: absolute;
    top: -8px; left: 22px;
    width: 14px; height: 14px;
    background: rgba(255,255,255,0.03);
    border-left: 1px solid rgba(129,140,248,0.15);
    border-top: 1px solid rgba(129,140,248,0.15);
    transform: rotate(45deg);
}
.typing-cursor {
    display: inline-block;
    width: 2px; height: 1em;
    background: #818cf8;
    margin-left: 2px;
    vertical-align: middle;
    animation: blink 0.8s step-end infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

/* Round badge on avatar card */
.round-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.9rem;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    border: 1px solid;
}

/* ────────────────────────────────────────────────
   CHAT AREA
──────────────────────────────────────────────── */
.chat-history {
    max-height: 320px;
    overflow-y: auto;
    padding: 0.5rem 0;
    margin-bottom: 1rem;
}
.chat-msg {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 1rem;
    animation: fadeSlideIn 0.3s ease forwards;
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.chat-msg.user { flex-direction: row-reverse; }
.chat-avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    border: 1.5px solid rgba(255,255,255,0.08);
}
.chat-avatar.ai  { background: linear-gradient(135deg, #1e213a, #252844); }
.chat-avatar.you { background: linear-gradient(135deg, #1a2535, #1e2f45); }
.chat-bubble {
    max-width: 85%;
    padding: 0.9rem 1.2rem;
    border-radius: 16px;
    font-size: 0.88rem;
    line-height: 1.65;
}
.chat-bubble.ai {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-top-left-radius: 4px;
    color: #cbd5e1;
    font-family: 'DM Mono', monospace !important;
    font-weight: 300;
}
.chat-bubble.you {
    background: linear-gradient(135deg, rgba(79,70,229,0.2), rgba(124,58,237,0.15));
    border: 1px solid rgba(129,140,248,0.2);
    border-top-right-radius: 4px;
    color: #e2e8f0;
}

/* ────────────────────────────────────────────────
   INPUT AREA
──────────────────────────────────────────────── */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
    font-weight: 300 !important;
    padding: 1rem !important;
    resize: none !important;
    transition: border-color 0.2s ease !important;
}
.stTextArea textarea:focus {
    border-color: rgba(129,140,248,0.4) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}
.stTextArea textarea::placeholder { color: #3d4060 !important; }
label[data-testid="stWidgetLabel"] { display: none !important; }

/* ────────────────────────────────────────────────
   BUTTONS
──────────────────────────────────────────────── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(79,70,229,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 30px rgba(79,70,229,0.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ────────────────────────────────────────────────
   UPLOAD ZONE
──────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1.5px dashed rgba(129,140,248,0.25) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(129,140,248,0.5) !important;
    background: rgba(99,102,241,0.04) !important;
}

/* ────────────────────────────────────────────────
   SCORE / FEEDBACK CARDS
──────────────────────────────────────────────── */
.score-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.score-number {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
    background: linear-gradient(135deg, #818cf8, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.score-label {
    font-size: 0.72rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.3rem;
}
.feedback-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.75rem;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0.25rem;
}
.pill-green {
    background: rgba(52,211,153,0.1);
    border: 1px solid rgba(52,211,153,0.25);
    color: #34d399;
}
.pill-amber {
    background: rgba(251,191,36,0.1);
    border: 1px solid rgba(251,191,36,0.25);
    color: #fbbf24;
}
.pill-red {
    background: rgba(248,113,113,0.1);
    border: 1px solid rgba(248,113,113,0.25);
    color: #f87171;
}

/* ────────────────────────────────────────────────
   LANDING / RESUME UPLOAD
──────────────────────────────────────────────── */
.landing-hero {
    text-align: center;
    padding: 3rem 2rem 2rem;
}
.landing-headline {
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #c7d2fe 0%, #a78bfa 50%, #67e8f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}
.landing-sub {
    font-size: 1rem;
    color: #64748b;
    max-width: 520px;
    margin: 0 auto 2.5rem;
    line-height: 1.7;
    font-weight: 400;
}
.feature-row {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 3rem;
    flex-wrap: wrap;
}
.feature-chip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 100px;
    font-size: 0.8rem;
    color: #94a3b8;
}

/* ────────────────────────────────────────────────
   RESUME SCORE CARD
──────────────────────────────────────────────── */
.resume-score-bar {
    height: 6px;
    background: #1e2030;
    border-radius: 10px;
    overflow: hidden;
    margin: 0.4rem 0;
}
.resume-score-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #4f46e5, #818cf8);
    transition: width 1s ease;
}

/* ────────────────────────────────────────────────
   FINAL REPORT
──────────────────────────────────────────────── */
.report-header {
    text-align: center;
    padding: 2.5rem;
    background: linear-gradient(135deg, #0d0f1e, #111428);
    border: 1px solid rgba(129,140,248,0.15);
    border-radius: 24px;
    margin-bottom: 1.5rem;
}
.verdict-badge {
    display: inline-block;
    padding: 0.4rem 1.2rem;
    border-radius: 100px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.verdict-hire { background: rgba(52,211,153,0.15); border: 1px solid #34d399; color: #34d399; }
.verdict-maybe { background: rgba(251,191,36,0.15); border: 1px solid #fbbf24; color: #fbbf24; }
.verdict-no { background: rgba(248,113,113,0.15); border: 1px solid #f87171; color: #f87171; }

.big-score {
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
    background: linear-gradient(135deg, #818cf8, #a78bfa, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.grade-letter {
    font-size: 2rem;
    font-weight: 700;
    color: #6366f1;
}

/* ────────────────────────────────────────────────
   MISC
──────────────────────────────────────────────── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
    margin: 1.5rem 0;
}
.section-title {
    font-size: 0.7rem;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.8rem;
}
[data-testid="stHorizontalBlock"] { gap: 1.2rem; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def api(method: str, path: str, **kwargs):
    try:
        r = requests.request(method, f"{API_BASE}{path}", timeout=60, **kwargs)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot reach the backend. Is the server running?")
        return None
    except Exception as e:
        st.error(f"API error: {e}")
        return None


def init_state():
    defaults = {
        "page": "landing",          # landing | interview | results
        "session_token": None,
        "resume_data": {},
        "resume_score": {},
        "current_round": "HR",
        "current_question": "",
        "question_number": 0,
        "chat_history": [],         # list of {role, content, round}
        "rounds_completed": [],
        "last_eval": None,
        "final_report": None,
        "is_speaking": False,
        "answer_input": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()


def render_header():
    st.markdown("""
    <div class="app-header">
        <div>
            <div class="app-logo">⬡ InterviewAI</div>
        </div>
        <div class="app-tagline">Multi-round · AI-powered · Real feedback</div>
    </div>
    """, unsafe_allow_html=True)


def render_round_progress(current_round, rounds_completed):
    steps_html = ""
    for i, r in enumerate(ROUNDS):
        is_done = r in rounds_completed
        is_active = r == current_round
        dot_class = "active" if is_active else ("done" if is_done else "")
        label_class = "active" if is_active else ("done" if is_done else "")
        icon = "✓" if is_done else ROUND_META[r]["icon"]
        connector_class = "done" if (i < len(ROUNDS) - 1 and ROUNDS[i + 1] in rounds_completed + [current_round]) else ""
        steps_html += f"""
        <div class="round-step">
            <div style="display:flex;flex-direction:column;align-items:center;">
                <div class="round-dot {dot_class}">{icon}</div>
                <div class="round-label {label_class}">{ROUND_META[r]['label']}</div>
            </div>
            {"" if i == len(ROUNDS) - 1 else f'<div class="round-connector {connector_class}"></div>'}
        </div>
        """
    st.markdown(f'<div class="round-progress">{steps_html}</div>', unsafe_allow_html=True)


def get_avatar_for_round(round_name):
    avatars = {"HR": "👩‍💼", "APTITUDE": "🧑‍🏫", "TECHNICAL": "👨‍💻", "DSA": "🤖"}
    names = {"HR": "Sarah Chen", "APTITUDE": "Prof. Arjun", "TECHNICAL": "Alex Rivera", "DSA": "Bot-9000"}
    titles = {"HR": "HR Manager", "APTITUDE": "Aptitude Examiner", "TECHNICAL": "Senior Engineer", "DSA": "Algorithm Specialist"}
    return avatars.get(round_name, "🤖"), names.get(round_name, "Interviewer"), titles.get(round_name, "Interviewer")


def render_avatar_card(round_name, question_text, is_speaking):
    emoji, name, title = get_avatar_for_round(round_name)
    meta = ROUND_META[round_name]
    speaking_class = "speaking" if is_speaking else ""
    wave_class = "active" if is_speaking else ""

    st.markdown(f"""
    <div class="avatar-card">
        <div class="round-badge" style="color:{meta['color']};border-color:{meta['color']}33;background:{meta['color']}11;">
            {meta['icon']} {meta['label']}
        </div>
        <div class="avatar-face {speaking_class}">{emoji}</div>
        <div class="sound-wave">
            {''.join(f'<div class="wave-bar {wave_class}" style="height:{h}px"></div>' for h in [6,10,16,20,24,20,16,10,6])}
        </div>
        <div class="avatar-name">{name}</div>
        <div class="avatar-title">{title}</div>
        <div class="speech-bubble">
            {question_text if question_text else '<span style="color:#3d4060">Preparing your question…</span>'}
            {'<span class="typing-cursor"></span>' if is_speaking else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_history(history, current_round):
    if not history:
        return
    filtered = [m for m in history if m.get("round") == current_round]
    if not filtered:
        return

    msgs_html = ""
    for msg in filtered[-8:]:
        if msg["role"] == "assistant":
            msgs_html += f"""
            <div class="chat-msg ai">
                <div class="chat-avatar ai">🤖</div>
                <div class="chat-bubble ai">{msg['content']}</div>
            </div>"""
        else:
            msgs_html += f"""
            <div class="chat-msg user">
                <div class="chat-avatar you">👤</div>
                <div class="chat-bubble you">{msg['content']}</div>
            </div>"""
    st.markdown(f'<div class="chat-history">{msgs_html}</div>', unsafe_allow_html=True)


def render_eval_feedback(ev):
    if not ev:
        return
    score = ev.get("score", 0)
    color = "#34d399" if score >= 7 else ("#fbbf24" if score >= 5 else "#f87171")
    st.markdown(f"""
    <div class="score-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
                <div class="score-number" style="background:linear-gradient(135deg,{color},{color}88);-webkit-background-clip:text;">{score}<span style="font-size:1.5rem">/10</span></div>
                <div class="score-label">Answer Score</div>
            </div>
            <div style="text-align:right;font-size:0.82rem;color:#94a3b8;max-width:60%;line-height:1.6;">
                {ev.get('feedback','')[:160]}
            </div>
        </div>
        <div class="divider"></div>
        <div>
            {''.join(f'<span class="feedback-pill pill-green">✓ {s}</span>' for s in ev.get('strengths',[]))}
            {''.join(f'<span class="feedback-pill pill-amber">↑ {s}</span>' for s in ev.get('improvements',[]))}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: LANDING
# ─────────────────────────────────────────────────────────────────────────────

def page_landing():
    render_header()

    st.markdown("""
    <div class="landing-hero">
        <div class="landing-headline">Ace your next<br>tech interview.</div>
        <div class="landing-sub">
            Practice with AI interviewers across HR, Aptitude, Technical, and DSA rounds.
            Get instant feedback personalised to your resume.
        </div>
        <div class="feature-row">
            <div class="feature-chip">👤 HR Behavioral</div>
            <div class="feature-chip">🧮 Aptitude Tests</div>
            <div class="feature-chip">💻 Technical Deep-dive</div>
            <div class="feature-chip">🔢 DSA Coding</div>
            <div class="feature-chip">📊 AI Scoring</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown('<div class="section-title">Upload Your Resume to Begin</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("resume", type=["pdf", "docx"], label_visibility="collapsed")

        if uploaded:
            st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
            if st.button("🚀  Parse Resume & Start Interview", use_container_width=True):
                with st.spinner("Reading your resume…"):
                    data = api("POST", "/resume/upload", files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)})
                if data:
                    st.session_state.session_token = data["session_token"]
                    st.session_state.resume_data = data["resume_data"]
                    st.session_state.resume_score = data.get("resume_score", {})
                    st.session_state.page = "resume_preview"
                    st.rerun()

    # Background ambient orbs
    st.markdown("""
    <div style="position:fixed;top:10%;left:5%;width:300px;height:300px;
                background:radial-gradient(circle,rgba(99,102,241,0.06) 0%,transparent 70%);
                pointer-events:none;z-index:0;border-radius:50%;"></div>
    <div style="position:fixed;bottom:15%;right:8%;width:250px;height:250px;
                background:radial-gradient(circle,rgba(167,139,250,0.05) 0%,transparent 70%);
                pointer-events:none;z-index:0;border-radius:50%;"></div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: RESUME PREVIEW
# ─────────────────────────────────────────────────────────────────────────────

def page_resume_preview():
    render_header()
    rd = st.session_state.resume_data
    rs = st.session_state.resume_score

    st.markdown('<div style="text-align:center;margin-bottom:1.5rem;">', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:1.8rem;font-weight:800;color:#c7d2fe;">Welcome, {rd.get("name","Candidate")} 👋</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.9rem;color:#64748b;margin-top:0.3rem;">Your resume has been parsed. Review your profile before starting the interview.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown('<div class="section-title">Parsed Profile</div>', unsafe_allow_html=True)

        skills = rd.get("technical_skills", rd.get("skills", []))
        if skills:
            skills_html = "".join(f'<span class="feedback-pill pill-green">{s}</span>' for s in skills[:12])
            st.markdown(f'<div style="margin-bottom:1rem;"><div style="font-size:0.75rem;color:#475569;margin-bottom:0.4rem;">SKILLS</div>{skills_html}</div>', unsafe_allow_html=True)

        projects = rd.get("projects", [])
        if projects:
            st.markdown('<div style="font-size:0.75rem;color:#475569;margin-bottom:0.6rem;">PROJECTS</div>', unsafe_allow_html=True)
            for p in projects[:3]:
                name = p.get("name", str(p)) if isinstance(p, dict) else str(p)
                desc = p.get("description", "") if isinstance(p, dict) else ""
                techs = p.get("technologies", []) if isinstance(p, dict) else []
                techs_html = "".join(f'<span style="font-size:0.65rem;background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.2);color:#818cf8;padding:0.15rem 0.5rem;border-radius:6px;margin-right:4px;">{t}</span>' for t in techs[:4])
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:0.9rem 1.1rem;margin-bottom:0.6rem;">
                    <div style="font-weight:600;color:#c7d2fe;font-size:0.88rem;margin-bottom:0.3rem;">📁 {name}</div>
                    <div style="font-size:0.78rem;color:#64748b;margin-bottom:0.4rem;line-height:1.5;">{desc[:100]}</div>
                    {techs_html}
                </div>
                """, unsafe_allow_html=True)

        exp = rd.get("experience", [])
        if exp:
            st.markdown('<div style="font-size:0.75rem;color:#475569;margin-top:0.8rem;margin-bottom:0.6rem;">EXPERIENCE</div>', unsafe_allow_html=True)
            for e in exp[:2]:
                role = e.get("role", "") if isinstance(e, dict) else str(e)
                company = e.get("company", "") if isinstance(e, dict) else ""
                dur = e.get("duration", "") if isinstance(e, dict) else ""
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:0.6rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                    <div>
                        <div style="font-size:0.88rem;font-weight:600;color:#cbd5e1;">{role}</div>
                        <div style="font-size:0.75rem;color:#64748b;">{company}</div>
                    </div>
                    <div style="font-size:0.72rem;color:#475569;">{dur}</div>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Resume Score</div>', unsafe_allow_html=True)
        pct = rs.get("percentage", 0)
        grade = rs.get("grade", "–")
        color = "#34d399" if pct >= 75 else ("#fbbf24" if pct >= 50 else "#f87171")

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:1.5rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
                <div>
                    <div style="font-size:3rem;font-weight:800;color:{color};line-height:1;">{pct:.0f}<span style="font-size:1.2rem">%</span></div>
                    <div style="font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:0.1em;">Resume Score</div>
                </div>
                <div style="width:60px;height:60px;border-radius:50%;background:rgba(99,102,241,0.1);border:2px solid rgba(99,102,241,0.3);display:flex;align-items:center;justify-content:center;font-size:1.5rem;font-weight:800;color:#818cf8;">{grade}</div>
            </div>
            <div class="resume-score-bar"><div class="resume-score-fill" style="width:{pct}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

        breakdown = rs.get("breakdown", {})
        for k, v in breakdown.items():
            max_vals = {"skills": 20, "projects": 25, "experience": 25, "education": 15, "contact": 10, "certifications": 5}
            mx = max_vals.get(k, 10)
            pct_b = (v / mx * 100) if mx else 0
            st.markdown(f"""
            <div style="margin-bottom:0.6rem;">
                <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#64748b;margin-bottom:0.25rem;">
                    <span>{k.capitalize()}</span><span>{v}/{mx}</span>
                </div>
                <div class="resume-score-bar"><div class="resume-score-fill" style="width:{pct_b}%;background:linear-gradient(90deg,#4f46e5,#818cf8);"></div></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
        feedback = rs.get("feedback", [])
        if feedback:
            st.markdown('<div class="section-title">Resume Tips</div>', unsafe_allow_html=True)
            for f in feedback[:4]:
                icon = "✓" if any(w in f.lower() for w in ["good", "great", "listed"]) else "→"
                color_f = "#34d399" if icon == "✓" else "#fbbf24"
                st.markdown(f'<div style="font-size:0.78rem;color:#94a3b8;padding:0.3rem 0;border-bottom:1px solid rgba(255,255,255,0.03);">'
                            f'<span style="color:{color_f}">{icon}</span> {f}</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        if st.button("🎤  Begin Interview", use_container_width=True):
            st.session_state.page = "interview"
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: INTERVIEW
# ─────────────────────────────────────────────────────────────────────────────

def page_interview():
    render_header()

    token = st.session_state.session_token
    current_round = st.session_state.current_round

    # Auto-start round if no question yet
    if not st.session_state.current_question:
        with st.spinner("Your interviewer is preparing…"):
            data = api("POST", "/interview/start", json={"session_token": token, "round_name": current_round})
        if data:
            st.session_state.current_question = data["question"]
            st.session_state.question_number = data["question_number"]
            st.session_state.is_speaking = True
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": data["question"],
                "round": current_round,
            })

    render_round_progress(current_round, st.session_state.rounds_completed)

    left_col, right_col = st.columns([5, 7], gap="large")

    # ── Left: Avatar ──────────────────────────────────────────────────────────
    with left_col:
        render_avatar_card(current_round, st.session_state.current_question, st.session_state.is_speaking)

        q_num = st.session_state.question_number
        total_q = 3
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;margin-top:0.8rem;padding:0 0.3rem;">
            <div style="font-size:0.72rem;color:#475569;">Question {q_num} of {total_q}</div>
            <div style="display:flex;gap:4px;">
                {''.join(f'<div style="width:20px;height:3px;border-radius:3px;background:{"#6366f1" if i < q_num else "#1e2030"};"></div>' for i in range(total_q))}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.last_eval:
            st.markdown('<div style="margin-top:1rem"></div>', unsafe_allow_html=True)
            render_eval_feedback(st.session_state.last_eval)

    # ── Right: Chat + Answer ──────────────────────────────────────────────────
    with right_col:
        st.markdown('<div class="section-title">Conversation</div>', unsafe_allow_html=True)
        render_chat_history(st.session_state.chat_history, current_round)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Your Answer</div>', unsafe_allow_html=True)

        answer = st.text_area(
            "answer",
            height=160,
            placeholder="Type your answer here… Be specific and structured.",
            key="answer_box",
            label_visibility="collapsed",
        )

        btn_col1, btn_col2 = st.columns([3, 1])
        with btn_col1:
            submit = st.button("Submit Answer  →", use_container_width=True)
        with btn_col2:
            skip = st.button("Skip", use_container_width=True)

        if submit or skip:
            final_answer = answer.strip() if (submit and answer.strip()) else "(skipped)"
            question = st.session_state.current_question

            with st.spinner("Evaluating…"):
                data = api("POST", "/interview/answer", json={
                    "session_token": token,
                    "answer": final_answer,
                    "question": question,
                    "round_name": current_round,
                })

            if data:
                st.session_state.last_eval = data["evaluation"]
                st.session_state.chat_history.append({"role": "user", "content": final_answer, "round": current_round})
                st.session_state.is_speaking = False

                if data.get("is_interview_complete"):
                    st.session_state.rounds_completed.append(current_round)
                    st.session_state.page = "results"
                    st.rerun()

                elif data.get("is_round_complete"):
                    st.session_state.rounds_completed.append(current_round)
                    next_r = data.get("next_round")
                    if next_r:
                        st.session_state.current_round = next_r
                        st.session_state.current_question = ""
                        st.session_state.question_number = 0
                        st.session_state.last_eval = None
                        st.session_state.is_speaking = False
                        meta = ROUND_META[next_r]
                        st.success(f"{meta['icon']} Round complete! Moving to **{meta['label']}**…")
                        time.sleep(1.5)
                        st.rerun()
                else:
                    nq = data.get("next_question")
                    if nq:
                        st.session_state.current_question = nq
                        st.session_state.question_number += 1
                        st.session_state.is_speaking = True
                        st.session_state.chat_history.append({"role": "assistant", "content": nq, "round": current_round})
                    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: RESULTS
# ─────────────────────────────────────────────────────────────────────────────

def page_results():
    render_header()

    token = st.session_state.session_token
    if not st.session_state.final_report:
        with st.spinner("Generating your final performance report…"):
            data = api("GET", f"/evaluation/results/{token}")
        if data:
            st.session_state.final_report = data

    report = st.session_state.final_report
    if not report:
        st.error("Could not load results.")
        return

    ff = report.get("final_feedback", {}) or {}
    overall = report.get("overall_score", 0)
    grade = ff.get("grade", "–")
    verdict = ff.get("verdict", "–")

    verdict_class = "verdict-hire" if "Recommended" in verdict and "Not" not in verdict else ("verdict-maybe" if "Maybe" in verdict else "verdict-no")

    # ── Report Header ─────────────────────────────────────────────────────────
    rd = report.get("resume_data") or st.session_state.resume_data or {}
    name = rd.get("name", "Candidate")
    st.markdown(f"""
    <div class="report-header">
        <div class="verdict-badge {verdict_class}">{verdict}</div>
        <div class="big-score">{overall:.1f}<span style="font-size:2rem;color:#6366f1">/10</span></div>
        <div style="font-size:0.9rem;color:#64748b;margin-top:0.5rem;">Overall Score · {name}</div>
        <div class="grade-letter" style="margin-top:0.5rem;">Grade: {grade}</div>
        <div style="font-size:0.88rem;color:#94a3b8;max-width:600px;margin:1rem auto 0;line-height:1.7;">
            {ff.get('executive_summary','Great effort across all four rounds!')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Round Scores Radar ────────────────────────────────────────────────────
    round_scores = report.get("round_scores", {})
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="section-title">Round Performance</div>', unsafe_allow_html=True)

        if round_scores:
            labels = [ROUND_META[r]["label"] for r in ROUNDS if r in round_scores]
            values = [round_scores.get(r, 0) for r in ROUNDS if r in round_scores]
            colors = [ROUND_META[r]["color"] for r in ROUNDS if r in round_scores]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=labels + [labels[0]],
                fill="toself",
                fillcolor="rgba(99,102,241,0.12)",
                line=dict(color="#818cf8", width=2),
                marker=dict(color="#818cf8", size=6),
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(255,255,255,0.06)", color="#3d4060", tickfont=dict(size=9)),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", color="#94a3b8"),
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=30, r=30, t=30, b=30),
                height=280,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        for r in ROUNDS:
            if r not in round_scores:
                continue
            s = round_scores[r]
            meta = ROUND_META[r]
            pct = s / 10 * 100
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.6rem;">
                <div style="font-size:1.1rem;">{meta['icon']}</div>
                <div style="flex:1;">
                    <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#94a3b8;margin-bottom:0.2rem;">
                        <span>{meta['label']}</span><span style="color:{meta['color']}">{s:.1f}/10</span>
                    </div>
                    <div class="resume-score-bar">
                        <div style="height:100%;width:{pct}%;background:{meta['color']};border-radius:10px;opacity:0.85;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        # Strengths
        st.markdown('<div class="section-title">Top Strengths</div>', unsafe_allow_html=True)
        for s in ff.get("top_strengths", []):
            st.markdown(f'<div style="display:flex;align-items:center;gap:0.6rem;padding:0.5rem 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:0.85rem;color:#94a3b8;"><span style="color:#34d399;font-size:1rem;">✓</span>{s}</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

        # Improvements
        st.markdown('<div class="section-title">Areas to Improve</div>', unsafe_allow_html=True)
        for i in ff.get("key_improvements", []):
            st.markdown(f'<div style="display:flex;align-items:center;gap:0.6rem;padding:0.5rem 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:0.85rem;color:#94a3b8;"><span style="color:#fbbf24;font-size:1rem;">↑</span>{i}</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

        # Next steps
        st.markdown('<div class="section-title">Recommended Next Steps</div>', unsafe_allow_html=True)
        for idx, step in enumerate(ff.get("next_steps", []), 1):
            st.markdown(f'<div style="display:flex;align-items:flex-start;gap:0.6rem;padding:0.5rem 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:0.85rem;color:#94a3b8;"><span style="color:#818cf8;font-weight:700;min-width:16px;">{idx}.</span>{step}</div>', unsafe_allow_html=True)

    # ── Round-by-round analysis ───────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Round-by-Round Analysis</div>', unsafe_allow_html=True)
    round_analysis = ff.get("round_analysis", {})
    round_details = report.get("round_details", {})

    for r in ROUNDS:
        if r not in round_scores:
            continue
        meta = ROUND_META[r]
        with st.expander(f"{meta['icon']} {meta['label']}  ·  {round_scores[r]:.1f}/10", expanded=False):
            st.markdown(f'<div style="font-size:0.85rem;color:#94a3b8;margin-bottom:1rem;">{round_analysis.get(r,"")}</div>', unsafe_allow_html=True)
            qas = round_details.get(r, {}).get("questions", [])
            for i, qa in enumerate(qas, 1):
                s = qa.get("score", 0)
                c = "#34d399" if s >= 7 else ("#fbbf24" if s >= 5 else "#f87171")
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:1rem;margin-bottom:0.7rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                        <div style="font-size:0.8rem;color:#475569;">Question {i}</div>
                        <div style="font-size:0.8rem;font-weight:700;color:{c};">{s:.1f}/10</div>
                    </div>
                    <div style="font-size:0.85rem;color:#cbd5e1;margin-bottom:0.5rem;font-family:'DM Mono',monospace;font-weight:300;">{qa.get('question','')}</div>
                    <div style="font-size:0.8rem;color:#64748b;font-style:italic;margin-bottom:0.4rem;">Your answer: {qa.get('answer','')[:200]}</div>
                    <div style="font-size:0.78rem;color:#94a3b8;">{qa.get('feedback','')}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────────────────────
    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        if st.button("🔄  Start a New Interview", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            init_state()
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────────────────────

page = st.session_state.page

if page == "landing":
    page_landing()
elif page == "resume_preview":
    page_resume_preview()
elif page == "interview":
    page_interview()
elif page == "results":
    page_results()
