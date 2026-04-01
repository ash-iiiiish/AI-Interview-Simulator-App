import os
import random
import requests
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
  "HR":        {"label": "HR Round",       "icon": "👤", "color": "#2563eb", "bg": "#eff6ff", "border": "#bfdbfe"},
  "APTITUDE":  {"label": "Aptitude Round",  "icon": "🧮", "color": "#d97706", "bg": "#fffbeb", "border": "#fde68a"},
  "TECHNICAL": {"label": "Technical Round", "icon": "💻", "color": "#059669", "bg": "#ecfdf5", "border": "#a7f3d0"},
  "DSA":       {"label": "DSA Round",       "icon": "🔢", "color": "#7c3aed", "bg": "#f5f3ff", "border": "#ddd6fe"},
}
INTERVIEWER_DATA = {
  "HR":        {"emoji": "👩‍💼", "name": "Sarah Chen",  "title": "HR Business Partner",   "company": "TechCorp Inc."},
  "APTITUDE":  {"emoji": "🧑‍🏫", "name": "Prof. Arjun", "title": "Assessment Specialist",  "company": "EvalPro Solutions"},
  "TECHNICAL": {"emoji": "👨‍💻", "name": "Alex Rivera",  "title": "Principal Engineer",     "company": "Silicon Labs"},
  "DSA":       {"emoji": "🤖",   "name": "ARIA-9",       "title": "Algorithm Intelligence", "company": "DeepCode AI"},
}
INTERVIEWER_GREETINGS = {
  "HR":        "Hi! I'm Sarah. Let's explore your background, motivations, and cultural fit. I want to hear your story — be yourself!",
  "APTITUDE":  "Hello! I'm Prof. Arjun. We'll work through logical and quantitative problems today. Take your time and think out loud.",
  "TECHNICAL": "Hey! Alex here. I'll probe your technical depth through practical scenarios. Think of it as a collaborative discussion.",
  "DSA":       "Initializing... ARIA-9 online. Algorithmic assessment mode: ACTIVE. Let us explore your problem-solving capabilities.",
}
FUN_FACTS = [
  "Candidates who do mock interviews are 3× more likely to receive an offer.",
  "The average tech interview has 5–7 rounds — preparation is everything.",
  "Structured STAR-method answers score 40% higher on average.",
  "Top candidates spend 10+ hours preparing before a major interview.",
  "85% of jobs are filled through networking, but interviews seal the deal.",
  "Interviewers form first impressions within the first 5 minutes.",
  "Speaking at a measured pace boosts perceived confidence by 32%.",
]

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;color:#111827!important}
#MainMenu,footer,header{visibility:hidden}
.stApp{background:#f8f7f4!important}
.block-container{padding:0!important;max-width:100%!important;margin:0!important}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:#f1f1f1}
::-webkit-scrollbar-thumb{background:#d1d5db;border-radius:4px}

/* NAVBAR */
.navbar{display:flex;align-items:center;justify-content:space-between;padding:1rem 3rem;background:#ffffff;border-bottom:1px solid #e5e7eb;position:sticky;top:0;z-index:100}
.nav-logo{font-family:'DM Sans',sans-serif;font-size:1.25rem;font-weight:700;color:#111827;letter-spacing:-0.03em;display:flex;align-items:center;gap:0.5rem}
.nav-logo .dot{width:8px;height:8px;background:#2563eb;border-radius:50%;display:inline-block}
.nav-right{display:flex;align-items:center;gap:0.6rem}
.npill{padding:0.3rem 0.85rem;border-radius:6px;font-size:0.72rem;font-family:'DM Mono',monospace;letter-spacing:0.01em;font-weight:500}
.npill-dim{background:#f3f4f6;color:#9ca3af;border:1px solid #e5e7eb}
.npill-blue{background:#eff6ff;color:#2563eb;border:1px solid #bfdbfe}

/* PAGE WRAPPER */
.page{padding:2.5rem 3rem 5rem;max-width:1400px;margin:0 auto}
.iv-page{padding:2rem 3rem 5rem;max-width:1400px;margin:0 auto}
.results-page{padding:2rem 3rem 5rem;max-width:1200px;margin:0 auto}

/* HERO */
.hero{background:#ffffff;border:1px solid #e5e7eb;border-radius:20px;padding:4rem;margin-bottom:2rem;position:relative;overflow:hidden}
.hero-label{display:inline-flex;align-items:center;gap:0.5rem;padding:0.35rem 1rem;background:#eff6ff;border:1px solid #bfdbfe;border-radius:6px;font-size:0.72rem;font-weight:600;color:#2563eb;margin-bottom:1.6rem;letter-spacing:0.06em;text-transform:uppercase}
.hero-title{font-family:'Instrument Serif',serif;font-size:4rem;font-weight:400;line-height:1.1;color:#111827;letter-spacing:-0.02em;margin-bottom:1.2rem}
.hero-title em{font-style:italic;color:#2563eb}
.hero-sub{font-size:1.05rem;color:#6b7280;line-height:1.7;max-width:540px;margin-bottom:2.5rem;font-weight:400}
.hero-stats{display:flex;gap:3rem}
.hstat-num{font-family:'Instrument Serif',serif;font-size:2.4rem;color:#111827;line-height:1}
.hstat-lbl{font-size:0.78rem;color:#9ca3af;margin-top:0.3rem;font-weight:500}
.hero-deco{position:absolute;right:3rem;top:50%;transform:translateY(-50%);width:280px;height:280px;border-radius:50%;background:linear-gradient(135deg,#eff6ff,#f5f3ff);border:1px solid #e5e7eb;display:flex;align-items:center;justify-content:center;font-size:5rem}

/* SECTION TITLES */
.sec-title{font-family:'Instrument Serif',serif;font-size:1.7rem;font-weight:400;color:#111827;margin-bottom:0.3rem;letter-spacing:-0.01em}
.sec-sub{font-size:0.88rem;color:#9ca3af;margin-bottom:1.5rem;font-weight:400}

/* ROUND CARDS */
.round-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:2rem}
.round-card{background:#ffffff;border:1px solid #e5e7eb;border-radius:16px;padding:1.8rem 1.5rem;transition:all 0.2s ease;cursor:default}
.round-card:hover{border-color:#d1d5db;transform:translateY(-3px);box-shadow:0 8px 30px rgba(0,0,0,0.07)}
.rc-icon-wrap{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;margin-bottom:1rem}
.rc-name{font-family:'DM Sans',sans-serif;font-size:0.95rem;font-weight:600;color:#111827;margin-bottom:0.35rem}
.rc-desc{font-size:0.8rem;color:#9ca3af;line-height:1.5}
.rc-tag{display:inline-block;margin-top:0.9rem;padding:0.2rem 0.65rem;border-radius:5px;font-size:0.68rem;font-family:'DM Mono',monospace;font-weight:500}

/* GREETER */
.greeter{background:#ffffff;border:1px solid #e5e7eb;border-radius:16px;padding:1.8rem 2rem;display:flex;align-items:center;gap:1.5rem;margin-bottom:1.5rem}
.greeter-emo-wrap{width:60px;height:60px;border-radius:14px;background:#f3f4f6;display:flex;align-items:center;justify-content:center;font-size:2rem;flex-shrink:0}
.gname{font-size:1rem;font-weight:600;color:#111827;margin-bottom:0.1rem}
.gtitle{font-size:0.75rem;color:#9ca3af;margin-bottom:0.5rem}
.gmsg{font-size:0.88rem;color:#6b7280;line-height:1.55;font-style:italic}

/* FUN FACT */
.funfact{background:#eff6ff;border:1px solid #bfdbfe;border-radius:16px;padding:1.4rem 2rem;display:flex;align-items:center;gap:1.2rem;margin-bottom:1.5rem}
.ff-icon{font-size:1.5rem;flex-shrink:0}
.ff-label{font-size:0.68rem;font-weight:700;color:#2563eb;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3rem}
.ff-text{font-size:0.9rem;color:#1e40af;line-height:1.5}

/* UPLOAD CARD */
.upload-card{background:#ffffff;border:1px solid #e5e7eb;border-radius:16px;padding:2rem 2rem 1.5rem;margin-bottom:1.5rem}
.uc-title{font-family:'Instrument Serif',serif;font-size:1.4rem;font-weight:400;color:#111827;margin-bottom:0.3rem}
.uc-sub{font-size:0.85rem;color:#9ca3af;margin-bottom:0}

[data-testid="stFileUploaderDropzone"]{background:#f8f7f4!important;border:2px dashed #d1d5db!important;border-radius:12px!important}
[data-testid="stFileUploaderDropzoneInstructions"] p{color:#9ca3af!important}
[data-testid="stFileUploaderDropzone"] svg{stroke:#d1d5db!important}
[data-testid="stFileUploaderDropzone"]:hover{border-color:#2563eb!important;background:#eff6ff!important}

/* BUTTONS */
.stButton>button{background:#111827!important;color:#ffffff!important;border:none!important;border-radius:10px!important;padding:0.8rem 1.5rem!important;font-weight:600!important;font-size:0.95rem!important;font-family:'DM Sans',sans-serif!important;letter-spacing:-0.01em!important;transition:all 0.2s ease!important;width:100%!important}
.stButton>button:hover{background:#1f2937!important;transform:translateY(-1px)!important;box-shadow:0 6px 20px rgba(17,24,39,0.15)!important}
.stButton>button:active{transform:translateY(0)!important}
.btn-primary .stButton>button{background:#2563eb!important}
.btn-primary .stButton>button:hover{background:#1d4ed8!important;box-shadow:0 6px 20px rgba(37,99,235,0.25)!important}
.btn-danger .stButton>button{background:#ffffff!important;color:#dc2626!important;border:1px solid #fca5a5!important}
.btn-danger .stButton>button:hover{background:#fef2f2!important;border-color:#f87171!important;box-shadow:none!important;transform:none!important}

/* PROGRESS BAR */
.prog-wrap{background:#ffffff;border:1px solid #e5e7eb;border-radius:60px;padding:1rem 2.5rem;margin:0 3rem 2rem;display:flex;align-items:center}
.prog-step{display:flex;align-items:center;flex:1}
.prog-node{display:flex;flex-direction:column;align-items:center;gap:0.4rem;flex-shrink:0}
.prog-circle{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.9rem;background:#f3f4f6;border:2px solid #e5e7eb;color:#9ca3af;transition:all 0.3s}
.prog-circle.done{background:#059669;border-color:#059669;color:white}
.prog-circle.active{background:#2563eb;border-color:#2563eb;color:white;box-shadow:0 0 0 4px #bfdbfe}
.prog-label{font-size:0.68rem;font-weight:600;color:#d1d5db;white-space:nowrap}
.prog-label.active{color:#2563eb}
.prog-label.done{color:#059669}
.prog-line{flex:1;height:2px;background:#e5e7eb;margin:0 0.5rem 1.2rem;border-radius:2px}
.prog-line.done{background:#059669}

/* INTERVIEW PANEL */
.iv-panel{background:#ffffff;border:1px solid #e5e7eb;border-radius:20px;overflow:hidden}
.iv-topbar{background:#f8f7f4;border-bottom:1px solid #e5e7eb;padding:0.85rem 1.5rem;display:flex;justify-content:space-between;align-items:center}
.iv-live{display:flex;align-items:center;gap:0.5rem;font-size:0.68rem;font-weight:700;color:#dc2626;letter-spacing:0.1em}
.recdot{width:7px;height:7px;background:#dc2626;border-radius:50%;animation:blink-dot 1.4s ease-in-out infinite}
@keyframes blink-dot{0%,100%{opacity:1}50%{opacity:0.2}}
.iv-badge{font-size:0.68rem;font-family:'DM Mono',monospace;color:#9ca3af;background:#f3f4f6;padding:0.2rem 0.75rem;border-radius:6px;border:1px solid #e5e7eb}
.iv-body{padding:2rem 1.5rem 1.5rem;text-align:center}
.iv-emo{width:100px;height:100px;border-radius:20px;background:#f3f4f6;border:1.5px solid #e5e7eb;display:flex;align-items:center;justify-content:center;font-size:3rem;margin:0 auto 1rem;transition:all 0.3s}
.iv-emo.speaking{border-color:#2563eb;box-shadow:0 0 0 4px #bfdbfe;background:#eff6ff}
.iv-name{font-family:'DM Sans',sans-serif;font-size:1.05rem;font-weight:700;color:#111827}
.iv-role{font-size:0.72rem;color:#9ca3af;margin-top:0.2rem}
.iv-co{font-size:0.72rem;color:#2563eb;margin-top:0.35rem;font-weight:500}
.iv-chips{display:flex;gap:0.5rem;justify-content:center;margin:1rem 0 1.2rem}
.ivchip{padding:0.25rem 0.8rem;background:#f3f4f6;border:1px solid #e5e7eb;border-radius:6px;font-size:0.7rem;font-family:'DM Mono',monospace;color:#6b7280}

/* QUESTION PANEL */
.q-panel{background:#ffffff;border:1px solid #e5e7eb;border-radius:20px;overflow:hidden}
.q-topbar{background:#f8f7f4;border-bottom:1px solid #e5e7eb;padding:0.85rem 1.5rem;display:flex;justify-content:space-between;align-items:center}
.q-head{font-size:0.68rem;color:#9ca3af;font-family:'DM Mono',monospace;font-weight:500}
.q-cpill{font-size:0.68rem;font-family:'DM Mono',monospace;color:#2563eb;background:#eff6ff;border:1px solid #bfdbfe;padding:0.2rem 0.75rem;border-radius:6px}
.q-bubble{margin:1.6rem;padding:1.5rem;background:#f8f7f4;border-left:3px solid #2563eb;border-radius:10px;font-size:0.92rem;line-height:1.7;color:#1f2937;font-family:'DM Sans',sans-serif}
.cursor{display:inline-block;width:2px;height:1em;background:#2563eb;margin-left:3px;animation:blink 1s step-end infinite;vertical-align:text-bottom}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
.qdots{display:flex;gap:0.5rem;padding:0 1.6rem 1.6rem}
.qdot{flex:1;height:3px;background:#e5e7eb;border-radius:4px}
.qdot.done{background:#059669}
.qdot.active{background:#2563eb}

/* CHAT */
.chat-wrap{background:#ffffff;border:1px solid #e5e7eb;border-radius:20px;padding:1.5rem}
.panel-label{font-size:0.68rem;font-weight:700;color:#9ca3af;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1.2rem;display:flex;align-items:center;gap:0.5rem}
.panel-label::before{content:'';width:3px;height:12px;background:#2563eb;border-radius:2px;display:inline-block}
.chat-scroll{max-height:380px;overflow-y:auto;padding-right:0.3rem}
.msg-row{display:flex;gap:0.7rem;margin-bottom:0.9rem;animation:fadein 0.3s ease}
@keyframes fadein{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg-row.user{flex-direction:row-reverse}
.msg-ava{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:0.85rem;flex-shrink:0;background:#f3f4f6;border:1px solid #e5e7eb}
.msg-ava.you{background:#eff6ff;border-color:#bfdbfe}
.mbubble{max-width:78%;padding:0.75rem 1rem;border-radius:12px;font-size:0.85rem;line-height:1.55}
.mbubble.ai{background:#f8f7f4;color:#374151;border-top-left-radius:4px;border:1px solid #e5e7eb}
.mbubble.you{background:#eff6ff;color:#1e40af;border-top-right-radius:4px;border:1px solid #bfdbfe}

/* INPUT */
.input-wrap{background:#ffffff;border:1px solid #e5e7eb;border-radius:20px;padding:1.5rem}
.stTextArea textarea{background:#f8f7f4!important;border:1.5px solid #e5e7eb!important;border-radius:10px!important;color:#111827!important;font-size:0.9rem!important;font-family:'DM Sans',sans-serif!important;padding:0.9rem!important;resize:vertical!important}
.stTextArea textarea::placeholder{color:#d1d5db!important}
.stTextArea textarea:focus{border-color:#2563eb!important;box-shadow:0 0 0 3px #bfdbfe!important;outline:none!important;background:#ffffff!important}
.stTextArea label{display:none!important}

/* RESULTS */
.r-banner{background:#ffffff;border:1px solid #e5e7eb;border-radius:20px;padding:3rem;text-align:center;margin-bottom:1.5rem}
.verdict-chip{display:inline-flex;align-items:center;padding:0.4rem 1.2rem;border-radius:6px;font-size:0.78rem;font-weight:700;letter-spacing:0.05em;margin-bottom:1.5rem}
.v-hire{background:#ecfdf5;color:#059669;border:1px solid #a7f3d0}
.v-maybe{background:#fffbeb;color:#d97706;border:1px solid #fde68a}
.v-no{background:#fef2f2;color:#dc2626;border:1px solid #fca5a5}
.r-score{font-family:'Instrument Serif',serif;font-size:6rem;font-weight:400;color:#111827;line-height:1;letter-spacing:-0.03em}
.r-score span{font-size:2rem;color:#9ca3af}
.r-grade{display:inline-block;margin:0.7rem auto;background:#f3f4f6;color:#6b7280;padding:0.3rem 1rem;border-radius:6px;font-size:0.8rem;font-weight:600}
.r-summary{font-size:0.95rem;color:#6b7280;max-width:540px;margin:0.8rem auto 0;line-height:1.65}
.r-card{background:#ffffff;border:1px solid #e5e7eb;border-radius:16px;padding:1.6rem;margin-bottom:1.2rem}
.r-card-title{font-size:0.72rem;font-weight:700;color:#9ca3af;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:1.2rem}
.bar-track{height:5px;background:#f3f4f6;border-radius:6px;overflow:hidden}
.bar-fill{height:100%;border-radius:6px;background:linear-gradient(90deg,#2563eb,#059669)}
.check-row{font-size:0.88rem;color:#374151;padding:0.55rem 0;border-bottom:1px solid #f3f4f6;display:flex;align-items:flex-start;gap:0.6rem}
</style>
""", unsafe_allow_html=True)


# ── API ────────────────────────────────────────────────────────────────────────
def api(method, path, **kwargs):
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


# ── State ──────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "landing", "session_token": None,
        "resume_data": {}, "resume_score": {},
        "current_round": "HR", "current_question": "",
        "question_number": 0, "chat_history": [],
        "rounds_completed": [], "last_eval": None,
        "final_report": None, "is_speaking": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Shared Components ──────────────────────────────────────────────────────────
def render_navbar(show_status=False):
    badge = ""
    if show_status and st.session_state.session_token:
        m = ROUND_META.get(st.session_state.current_round, {})
        badge = f'<span class="npill npill-blue">{m.get("icon","🎯")} {m.get("label","")}</span>'
    st.markdown(
        f'<div class="navbar"><div class="nav-logo"><span class="dot"></span>InterviewAI</div>'
        f'<div class="nav-right">{badge}'
        f'<span class="npill npill-dim">Powered by Groq</span>'
        f'<span class="npill npill-dim">llama-3.3-70b</span>'
        f'</div></div>',
        unsafe_allow_html=True
    )


def render_progress(current_round, rounds_completed):
    steps = ""
    for i, r in enumerate(ROUNDS):
        done   = r in rounds_completed
        active = r == current_round and not done
        cc = "active" if active else ("done" if done else "")
        lc = "active" if active else ("done" if done else "")
        icon = "✓" if done else ROUND_META[r]["icon"]
        ld = done or (i < len(ROUNDS)-1 and (ROUNDS[i+1] in rounds_completed or ROUNDS[i+1] == current_round))
        conn = f'<div class="prog-line {"done" if ld else ""}"></div>' if i < len(ROUNDS)-1 else ""
        steps += (f'<div class="prog-step"><div class="prog-node">'
                  f'<div class="prog-circle {cc}">{icon}</div>'
                  f'<div class="prog-label {lc}">{ROUND_META[r]["label"]}</div>'
                  f'</div>{conn}</div>')
    st.markdown(f'<div class="prog-wrap">{steps}</div>', unsafe_allow_html=True)


def render_interviewer_panel(round_name, question, q_num, total_q=5):
    meta = ROUND_META.get(round_name, {})
    iv   = INTERVIEWER_DATA.get(round_name, {})
    sp   = "speaking" if st.session_state.is_speaking else ""
    dots = "".join(
        f'<div class="qdot {"done" if i < q_num else "active" if i == q_num else ""}"></div>'
        for i in range(total_q)
    )
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown(
            f'<div class="iv-panel">'
            f'<div class="iv-topbar"><div class="iv-live"><div class="recdot"></div>LIVE</div>'
            f'<div class="iv-badge">{meta.get("label","")}</div></div>'
            f'<div class="iv-body"><div class="iv-emo {sp}">{iv.get("emoji","🤖")}</div>'
            f'<div class="iv-name">{iv.get("name","")}</div>'
            f'<div class="iv-role">{iv.get("title","")}</div>'
            f'<div class="iv-co">{iv.get("company","")}</div></div>'
            f'<div class="iv-chips">'
            f'<div class="ivchip">🎯 {meta.get("label","")}</div>'
            f'<div class="ivchip">📋 Q{q_num+1}/{total_q}</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div class="q-panel">'
            f'<div class="q-topbar"><div class="q-head">CURRENT QUESTION</div>'
            f'<div class="q-cpill">Q{q_num+1} / {total_q}</div></div>'
            f'<div class="q-bubble">{question}<span class="cursor"></span></div>'
            f'<div class="qdots">{dots}</div></div>',
            unsafe_allow_html=True
        )


def render_chat(chat_history):
    msgs = ""
    for m in chat_history:
        if m["role"] == "assistant":
            msgs += (f'<div class="msg-row"><div class="msg-ava">🤖</div>'
                     f'<div class="mbubble ai">{m["content"]}</div></div>')
        else:
            msgs += (f'<div class="msg-row user"><div class="msg-ava you">👤</div>'
                     f'<div class="mbubble you">{m["content"]}</div></div>')
    st.markdown(
        f'<div class="chat-wrap"><div class="panel-label">Conversation Log</div>'
        f'<div class="chat-scroll">{msgs}</div></div>',
        unsafe_allow_html=True
    )


# ── Pages ──────────────────────────────────────────────────────────────────────
def landing_page():
    render_navbar()
    st.markdown('<div class="page">', unsafe_allow_html=True)

    # Hero
    st.markdown(
        '<div class="hero">'
        '<div class="hero-label">✦ AI-Powered Mock Interviews</div>'
        '<div class="hero-title">Master Every Round.<br>Land Your <em>Dream Job.</em></div>'
        '<div class="hero-sub">Practice with AI interviewers across HR, Aptitude, Technical, and DSA rounds. '
        'Get real-time scoring and detailed reports to close the gap between where you are and where you want to be.</div>'
        '<div class="hero-stats">'
        '<div><div class="hstat-num">4</div><div class="hstat-lbl">Interview Rounds</div></div>'
        '<div><div class="hstat-num">20+</div><div class="hstat-lbl">Questions / Session</div></div>'
        '<div><div class="hstat-num">AI</div><div class="hstat-lbl">Real-time Feedback</div></div>'
        '<div><div class="hstat-num">3×</div><div class="hstat-lbl">Offer Likelihood</div></div>'
        '</div>'
        '<div class="hero-deco">🎯</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # Round Cards
    st.markdown('<div class="sec-title">What You\'ll Be Tested On</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Each round is tailored to your resume and real-world standards of top companies.</div>', unsafe_allow_html=True)
    descs = {
        "HR":        "Behavioural questions, leadership stories, culture fit assessments, and motivation deep-dives.",
        "APTITUDE":  "Quantitative reasoning, logical puzzles, data interpretation, and verbal ability.",
        "TECHNICAL": "Domain-specific knowledge, system design concepts, and project-based scenarios.",
        "DSA":       "Arrays, trees, graphs, dynamic programming, and algorithm complexity analysis.",
    }
    cards = "".join(
        f'<div class="round-card">'
        f'<div class="rc-icon-wrap" style="background:{ROUND_META[r]["bg"]}">{ROUND_META[r]["icon"]}</div>'
        f'<div class="rc-name">{ROUND_META[r]["label"]}</div>'
        f'<div class="rc-desc">{descs[r]}</div>'
        f'<span class="rc-tag" style="background:{ROUND_META[r]["bg"]};color:{ROUND_META[r]["color"]};border:1px solid {ROUND_META[r]["border"]}">{r}</span>'
        f'</div>'
        for r in ROUNDS
    )
    st.markdown(f'<div class="round-grid">{cards}</div>', unsafe_allow_html=True)

    # Greeter
    iv = INTERVIEWER_DATA["HR"]
    st.markdown(
        f'<div class="greeter"><div class="greeter-emo-wrap">{iv["emoji"]}</div>'
        f'<div><div class="gname">{iv["name"]} — Your First Interviewer</div>'
        f'<div class="gtitle">{iv["title"]} · {iv["company"]}</div>'
        f'<div class="gmsg">"{INTERVIEWER_GREETINGS["HR"]}"</div></div></div>',
        unsafe_allow_html=True
    )

    # Fun Fact
    fact = random.choice(FUN_FACTS)
    st.markdown(
        f'<div class="funfact"><div class="ff-icon">💡</div>'
        f'<div><div class="ff-label">Did You Know?</div>'
        f'<div class="ff-text">{fact}</div></div></div>',
        unsafe_allow_html=True
    )

    # Upload
    st.markdown(
        '<div class="upload-card">'
        '<div class="uc-title">Upload Your Resume to Begin</div>'
        '<div class="uc-sub">We\'ll personalise every question to your experience, skills, and the roles you\'re targeting.</div>'
        '</div>',
        unsafe_allow_html=True
    )
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)", type=["pdf"],
        key="resume_upload", label_visibility="collapsed",
    )
    if uploaded_file:
        files = {"file": ("resume.pdf", uploaded_file.getvalue(), "application/pdf")}
        result = api("POST", "/analyze-resume", files=files)
        if result:
            st.session_state.resume_data  = result.get("resume_data", {})
            st.session_state.resume_score = result.get("score", {})
            st.session_state.page = "interview"
            st.rerun()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Start Practice Session →", use_container_width=True):
            if not uploaded_file:
                st.warning("Please upload your resume first.")
            else:
                init_data = api("POST", "/init-session", json={"resume_data": st.session_state.resume_data})
                if init_data:
                    st.session_state.session_token    = init_data.get("session_token")
                    st.session_state.current_round    = init_data.get("current_round", "HR")
                    st.session_state.current_question = init_data.get("question", "Tell me about yourself.")
                    st.session_state.chat_history     = [{"role": "assistant", "content": st.session_state.current_question}]
                    st.session_state.page = "interview"
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def interview_page():
    render_navbar(show_status=True)
    render_progress(st.session_state.current_round, st.session_state.rounds_completed)
    st.markdown('<div class="iv-page">', unsafe_allow_html=True)

    rnd = st.session_state.current_round
    iv  = INTERVIEWER_DATA[rnd]
    st.markdown(
        f'<div class="greeter" style="margin-bottom:1.8rem">'
        f'<div class="greeter-emo-wrap">{iv["emoji"]}</div>'
        f'<div><div class="gname">{iv["name"]}</div>'
        f'<div class="gtitle">{iv["title"]} · {iv["company"]}</div>'
        f'<div class="gmsg">"{INTERVIEWER_GREETINGS[rnd]}"</div>'
        f'</div></div>',
        unsafe_allow_html=True
    )

    render_interviewer_panel(
        st.session_state.current_round,
        st.session_state.current_question,
        st.session_state.question_number, 5,
    )
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    col_chat, col_input = st.columns([3, 2], gap="medium")
    with col_chat:
        render_chat(st.session_state.chat_history)

    with col_input:
        st.markdown('<div class="input-wrap"><div class="panel-label">Your Answer</div>', unsafe_allow_html=True)
        answer = st.text_area("ans", height=220, key="answer_input",
                              label_visibility="collapsed",
                              placeholder="Type your answer here…")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            submit = st.button("✅ Submit", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b2:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            end = st.button("⏹ End Session", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if end:
            report = api("POST", "/final-report", json={"session_token": st.session_state.session_token})
            if report:
                st.session_state.final_report = report
                st.session_state.page = "results"
                st.rerun()

        if submit and answer:
            st.session_state.chat_history.append({"role": "user", "content": answer})
            st.session_state.is_speaking = True
            ev = api("POST", "/evaluate", json={
                "session_token": st.session_state.session_token,
                "answer": answer,
                "round_name": st.session_state.current_round,
            })
            if ev:
                st.session_state.last_eval = ev
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"📊 Score: {ev.get('score',0)}/10\n\n💡 {ev.get('feedback','')}",
                })
                if ev.get("move_next", False):
                    nq = api("POST", "/next-question", json={"session_token": st.session_state.session_token})
                    if nq:
                        if nq.get("round_completed", False):
                            st.session_state.rounds_completed.append(st.session_state.current_round)
                            idx = ROUNDS.index(st.session_state.current_round) + 1
                            if idx < len(ROUNDS):
                                st.session_state.current_round    = ROUNDS[idx]
                                st.session_state.question_number  = 0
                                st.session_state.current_question = nq.get("question", "")
                                st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.current_question})
                            else:
                                rpt = api("POST", "/final-report", json={"session_token": st.session_state.session_token})
                                if rpt:
                                    st.session_state.final_report = rpt
                                    st.session_state.page = "results"
                        else:
                            st.session_state.current_question = nq.get("question", "")
                            st.session_state.question_number += 1
                            st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.current_question})
            st.session_state.is_speaking = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def results_page():
    render_navbar()
    report = st.session_state.final_report
    if not report:
        st.error("No report available.")
        if st.button("Start New Session"):
            st.session_state.page = "landing"
            st.rerun()
        return

    overall = report.get("overall_score", 0)
    grade   = report.get("grade", "C")
    verdict = report.get("verdict", "Consider")
    summary = report.get("summary", "")

    if "hire" in verdict.lower():
        vc, vt = "v-hire",  "✓ Recommended for Hire"
    elif "consider" in verdict.lower():
        vc, vt = "v-maybe", "→ Consider for Next Round"
    else:
        vc, vt = "v-no",    "✗ Needs Improvement"

    st.markdown('<div class="results-page">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="r-banner">'
        f'<div class="verdict-chip {vc}">{vt}</div>'
        f'<div class="r-score">{overall}<span>/100</span></div>'
        f'<div class="r-grade">Grade {grade}</div>'
        f'<div class="r-summary">{summary}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="medium")
    rs = report.get("round_scores", {})
    with col1:
        st.markdown('<div class="r-card"><div class="r-card-title">Round-wise Performance</div>', unsafe_allow_html=True)
        for r in ROUNDS:
            score = rs.get(r, 0)
            pct   = (score / 10) * 100 if score <= 10 else score
            st.markdown(
                f'<div style="margin-bottom:1.2rem">'
                f'<div style="display:flex;justify-content:space-between;font-size:0.85rem;color:#6b7280;margin-bottom:0.4rem">'
                f'<span>{ROUND_META[r]["icon"]} {ROUND_META[r]["label"]}</span>'
                f'<strong style="color:#111827">{score}/10</strong></div>'
                f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        strengths = report.get("strengths", ["Communication Skills", "Technical Knowledge", "Problem Solving"])[:3]
        improve   = report.get("improvements", ["Practice more", "Structure answers better", "Time management"])[:3]
        s_html = "".join(f'<div class="check-row">✅ {s}</div>' for s in strengths)
        i_html = "".join(f'<div class="check-row">🎯 {i}</div>' for i in improve)
        st.markdown(
            f'<div class="r-card"><div class="r-card-title">Key Strengths</div>{s_html}'
            f'<div class="r-card-title" style="margin-top:1.4rem">Areas for Improvement</div>{i_html}</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("🔄 Start New Session", use_container_width=True):
            for k in ["session_token","resume_data","resume_score","current_round","current_question",
                      "question_number","chat_history","rounds_completed","last_eval","final_report"]:
                st.session_state.pop(k, None)
            st.session_state.page = "landing"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ── Router ─────────────────────────────────────────────────────────────────────
if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "interview":
    interview_page()
elif st.session_state.page == "results":
    results_page()