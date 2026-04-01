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
  "HR":        {"label": "HR Round",       "icon": "👤", "color": "#1a1a1a", "bg": "#f5e6d3", "accent": "#e8845a"},
  "APTITUDE":  {"label": "Aptitude Round",  "icon": "🧮", "color": "#1a1a1a", "bg": "#d4e8d4", "accent": "#4a9e6b"},
  "TECHNICAL": {"label": "Technical Round", "icon": "💻", "color": "#1a1a1a", "bg": "#d4d4e8", "accent": "#6b5fa6"},
  "DSA":       {"label": "DSA Round",       "icon": "🔢", "color": "#1a1a1a", "bg": "#3d1f1f", "accent": "#e8845a"},
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=Figtree:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'Figtree',sans-serif!important;color:#1a1a1a!important}
#MainMenu,footer,header{visibility:hidden}
.stApp{background:#faf9f6!important}
.block-container{padding:0!important;max-width:100%!important;margin:0!important}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:#f0ede8}
::-webkit-scrollbar-thumb{background:#c9c4bc;border-radius:4px}

/* NAVBAR */
.navbar{display:flex;align-items:center;justify-content:space-between;padding:1rem 3.5rem;background:#ffffff;border-bottom:1px solid #e8e3dc;position:sticky;top:0;z-index:200}
.nav-logo{font-family:'Fraunces',serif;font-size:1.35rem;font-weight:600;color:#1a1a1a;letter-spacing:-0.03em;display:flex;align-items:center;gap:0.55rem}
.nav-logo-icon{width:28px;height:28px;background:#1a1a1a;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:0.85rem}
.nav-links{display:flex;align-items:center;gap:2.5rem}
.nav-link{font-size:0.88rem;color:#6b6560;font-weight:500;cursor:pointer;transition:color 0.2s}
.nav-link:hover{color:#1a1a1a}
.nav-right{display:flex;align-items:center;gap:0.8rem}
.nav-btn-ghost{padding:0.45rem 1.1rem;border-radius:8px;font-size:0.85rem;font-weight:600;color:#1a1a1a;border:1.5px solid #e8e3dc;background:transparent}
.nav-btn-solid{padding:0.45rem 1.2rem;border-radius:8px;font-size:0.85rem;font-weight:600;color:#ffffff;background:#1a1a1a}
.nav-badge{display:flex;align-items:center;gap:0.4rem;padding:0.3rem 0.85rem;background:#fdf0e8;border:1px solid #f0d0b8;border-radius:6px;font-size:0.72rem;font-family:'JetBrains Mono',monospace;color:#e8845a}

/* PAGE */
.page{padding:0 0 6rem}
.iv-page{padding:2rem 3.5rem 5rem;max-width:1400px;margin:0 auto}
.results-page{padding:2rem 3.5rem 5rem;max-width:1200px;margin:0 auto}

/* HERO */
.hero-section{padding:5rem 3.5rem 3.5rem;background:#ffffff;text-align:center;border-bottom:1px solid #e8e3dc}
.hero-pill{display:inline-flex;align-items:center;gap:0.5rem;padding:0.35rem 1rem;background:#f5f0e8;border:1px solid #e8ddd0;border-radius:100px;font-size:0.75rem;font-weight:600;color:#8a7060;margin-bottom:1.8rem;letter-spacing:0.04em}
.hero-pill-dot{width:6px;height:6px;background:#e8845a;border-radius:50%;display:inline-block}
.hero-title{font-family:'Fraunces',serif;font-size:4.8rem;font-weight:300;line-height:1.05;color:#1a1a1a;letter-spacing:-0.04em;margin-bottom:1.2rem;max-width:820px;margin-left:auto;margin-right:auto}
.hero-title em{font-style:italic;color:#e8845a}
.hero-title strong{font-weight:600}
.hero-sub{font-size:1.05rem;color:#8a8078;line-height:1.7;max-width:500px;margin:0 auto 3rem;font-weight:400}
.hero-stats-row{display:flex;align-items:stretch;justify-content:center;gap:0;border:1px solid #e8e3dc;border-radius:16px;overflow:hidden;max-width:700px;margin:0 auto}
.hstat{flex:1;padding:1.4rem 2rem;background:#ffffff;text-align:center;border-right:1px solid #e8e3dc}
.hstat:last-child{border-right:none}
.hstat-num{font-family:'Fraunces',serif;font-size:2rem;font-weight:600;color:#1a1a1a;letter-spacing:-0.03em}
.hstat-lbl{font-size:0.75rem;color:#a09890;margin-top:0.3rem;font-weight:500}

/* CARDS GRID */
.cards-section{padding:2.5rem 3.5rem;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto auto;gap:1.2rem}
.feature-card{border-radius:20px;padding:2.5rem;position:relative;overflow:hidden;min-height:270px;display:flex;flex-direction:column;justify-content:space-between;transition:transform 0.2s ease}
.feature-card:hover{transform:translateY(-3px)}
.fc-warm{background:#f5e6d3}
.fc-green{background:#d4e8d4}
.fc-dark{background:#1a1a1a}
.fc-purple{background:#e8e4f5}
.fc-title{font-family:'Fraunces',serif;font-size:1.85rem;font-weight:400;line-height:1.2;letter-spacing:-0.02em}
.fc-warm .fc-title,.fc-green .fc-title,.fc-purple .fc-title{color:#1a1a1a}
.fc-dark .fc-title{color:#ffffff;font-size:2rem}
.fc-sub{font-size:0.87rem;line-height:1.6;margin-top:0.5rem}
.fc-warm .fc-sub,.fc-green .fc-sub,.fc-purple .fc-sub{color:#6b6055}
.fc-dark .fc-sub{color:#9a9590}
.fc-badge{display:inline-flex;align-items:center;gap:0.4rem;padding:0.28rem 0.85rem;border-radius:100px;font-size:0.72rem;font-weight:600;margin-bottom:0.9rem;width:fit-content}
.fc-warm .fc-badge{background:rgba(232,132,90,0.2);color:#b05020}
.fc-green .fc-badge{background:rgba(74,158,107,0.2);color:#2a7e4b}
.fc-dark .fc-badge{background:rgba(255,255,255,0.1);color:#b0acaa}
.fc-purple .fc-badge{background:rgba(107,95,166,0.2);color:#4a3e8a}
.fc-emoji{font-size:4rem;position:absolute;right:2rem;bottom:1.8rem;opacity:0.28}
.fc-stat-float{position:absolute;bottom:1.5rem;left:2.5rem;background:rgba(255,255,255,0.88);border-radius:12px;padding:0.65rem 1rem;backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.6)}
.fc-stat-float .num{font-family:'Fraunces',serif;font-size:1.35rem;font-weight:600;color:#1a1a1a;line-height:1}
.fc-stat-float .lbl{font-size:0.65rem;color:#8a8078;font-weight:500;margin-top:0.15rem}
.fc-tags{display:flex;flex-wrap:wrap;gap:0.45rem;margin-top:0.9rem}
.fc-tag{padding:0.22rem 0.65rem;background:rgba(255,255,255,0.5);border:1px solid rgba(0,0,0,0.1);border-radius:100px;font-size:0.68rem;font-weight:500;color:#4a4440}
.fc-dark .fc-tag{background:rgba(255,255,255,0.07);border-color:rgba(255,255,255,0.1);color:#c0bcb8}

/* UPLOAD */
.upload-section{margin:0 3.5rem 2rem;background:#ffffff;border:1px solid #e8e3dc;border-radius:20px;padding:2.5rem 3rem;display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start}
.us-title{font-family:'Fraunces',serif;font-size:2.1rem;font-weight:400;color:#1a1a1a;letter-spacing:-0.02em;line-height:1.2;margin-bottom:0.6rem}
.us-sub{font-size:0.88rem;color:#8a8078;line-height:1.6;margin-bottom:1rem}
.us-points{display:flex;flex-direction:column;gap:0.5rem}
.us-point{display:flex;align-items:center;gap:0.6rem;font-size:0.84rem;color:#4a4440;font-weight:500}
.us-check{width:20px;height:20px;background:#d4e8d4;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:0.65rem;flex-shrink:0;color:#2a7e4b;font-weight:700}

/* FUN FACT */
.funfact-bar{margin:0 3.5rem 1.5rem;background:linear-gradient(135deg,#1a1a1a 0%,#2d2520 100%);border-radius:16px;padding:1.4rem 2rem;display:flex;align-items:center;gap:1.2rem}
.ff-icon{font-size:1.4rem;flex-shrink:0}
.ff-label{font-size:0.65rem;font-weight:700;color:#e8845a;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.25rem}
.ff-text{font-size:0.9rem;color:#e8e3dc;line-height:1.5}

/* BUTTONS */
.stButton>button{background:#1a1a1a!important;color:#ffffff!important;border:none!important;border-radius:10px!important;padding:0.8rem 1.5rem!important;font-weight:600!important;font-size:0.95rem!important;font-family:'Figtree',sans-serif!important;transition:all 0.2s ease!important;width:100%!important}
.stButton>button:hover{background:#2d2520!important;transform:translateY(-1px)!important;box-shadow:0 6px 20px rgba(26,26,26,0.18)!important}
.btn-orange .stButton>button{background:#e8845a!important;color:#ffffff!important}
.btn-orange .stButton>button:hover{background:#d46840!important;box-shadow:0 6px 20px rgba(232,132,90,0.3)!important}
.btn-ghost .stButton>button{background:#ffffff!important;color:#1a1a1a!important;border:1.5px solid #e8e3dc!important}
.btn-ghost .stButton>button:hover{background:#f5f0e8!important;box-shadow:none!important;transform:none!important}
.btn-danger .stButton>button{background:#ffffff!important;color:#c04040!important;border:1.5px solid #f0caca!important}
.btn-danger .stButton>button:hover{background:#fef2f2!important;box-shadow:none!important;transform:none!important}

/* PROGRESS */
.prog-wrap{background:#ffffff;border-bottom:1px solid #e8e3dc;padding:1rem 3.5rem;display:flex;align-items:center;position:sticky;top:65px;z-index:100}
.prog-step{display:flex;align-items:center;flex:1}
.prog-node{display:flex;flex-direction:column;align-items:center;gap:0.35rem;flex-shrink:0}
.prog-circle{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.85rem;background:#f0ede8;border:2px solid #e8e3dc;color:#a09890;transition:all 0.3s}
.prog-circle.done{background:#4a9e6b;border-color:#4a9e6b;color:white}
.prog-circle.active{background:#e8845a;border-color:#e8845a;color:white;box-shadow:0 0 0 4px rgba(232,132,90,0.2)}
.prog-label{font-size:0.65rem;font-weight:600;color:#c0bcb8;white-space:nowrap}
.prog-label.active{color:#e8845a}
.prog-label.done{color:#4a9e6b}
.prog-line{flex:1;height:2px;background:#e8e3dc;margin:0 0.5rem 1.2rem;border-radius:2px}
.prog-line.done{background:#4a9e6b}

/* GREETER */
.greeter{background:#ffffff;border:1px solid #e8e3dc;border-radius:16px;padding:1.5rem 2rem;display:flex;align-items:center;gap:1.5rem;margin-bottom:1.5rem}
.greeter-emo-wrap{width:54px;height:54px;border-radius:13px;background:#f5f0e8;display:flex;align-items:center;justify-content:center;font-size:1.8rem;flex-shrink:0;border:1px solid #e8e3dc}
.gname{font-family:'Fraunces',serif;font-size:1rem;font-weight:600;color:#1a1a1a;margin-bottom:0.1rem}
.gtitle{font-size:0.72rem;color:#a09890;margin-bottom:0.45rem}
.gmsg{font-size:0.86rem;color:#6b6055;line-height:1.55;font-style:italic}

/* IV PANEL */
.iv-panel{background:#ffffff;border:1px solid #e8e3dc;border-radius:20px;overflow:hidden}
.iv-topbar{background:#f5f0e8;border-bottom:1px solid #e8e3dc;padding:0.85rem 1.5rem;display:flex;justify-content:space-between;align-items:center}
.iv-live{display:flex;align-items:center;gap:0.5rem;font-size:0.68rem;font-weight:700;color:#c04040;letter-spacing:0.1em}
.recdot{width:7px;height:7px;background:#c04040;border-radius:50%;animation:blink-dot 1.4s ease-in-out infinite}
@keyframes blink-dot{0%,100%{opacity:1}50%{opacity:0.2}}
.iv-badge{font-size:0.68rem;font-family:'JetBrains Mono',monospace;color:#8a8078;background:#ede9e2;padding:0.2rem 0.75rem;border-radius:6px;border:1px solid #ddd8d0}
.iv-body{padding:2rem 1.5rem 1.5rem;text-align:center}
.iv-emo{width:96px;height:96px;border-radius:18px;background:#f5f0e8;border:1.5px solid #e8e3dc;display:flex;align-items:center;justify-content:center;font-size:3rem;margin:0 auto 1rem;transition:all 0.3s}
.iv-emo.speaking{border-color:#e8845a;box-shadow:0 0 0 4px rgba(232,132,90,0.18);background:#fdf0e8}
.iv-name{font-family:'Fraunces',serif;font-size:1.1rem;font-weight:600;color:#1a1a1a}
.iv-role{font-size:0.72rem;color:#a09890;margin-top:0.2rem}
.iv-co{font-size:0.72rem;color:#e8845a;margin-top:0.35rem;font-weight:600}
.iv-chips{display:flex;gap:0.5rem;justify-content:center;margin:1rem 0 1.2rem}
.ivchip{padding:0.25rem 0.8rem;background:#f0ede8;border:1px solid #e8e3dc;border-radius:6px;font-size:0.7rem;font-family:'JetBrains Mono',monospace;color:#6b6560}

/* QUESTION PANEL */
.q-panel{background:#ffffff;border:1px solid #e8e3dc;border-radius:20px;overflow:hidden}
.q-topbar{background:#f5f0e8;border-bottom:1px solid #e8e3dc;padding:0.85rem 1.5rem;display:flex;justify-content:space-between;align-items:center}
.q-head{font-size:0.68rem;color:#a09890;font-family:'JetBrains Mono',monospace;font-weight:500}
.q-cpill{font-size:0.68rem;font-family:'JetBrains Mono',monospace;color:#e8845a;background:#fdf0e8;border:1px solid #f0d0b8;padding:0.2rem 0.75rem;border-radius:6px}
.q-bubble{margin:1.6rem;padding:1.5rem;background:#f5f0e8;border-left:3px solid #e8845a;border-radius:10px;font-size:0.92rem;line-height:1.7;color:#2d2520}
.cursor{display:inline-block;width:2px;height:1em;background:#e8845a;margin-left:3px;animation:blink 1s step-end infinite;vertical-align:text-bottom}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
.qdots{display:flex;gap:0.5rem;padding:0 1.6rem 1.6rem}
.qdot{flex:1;height:3px;background:#e8e3dc;border-radius:4px}
.qdot.done{background:#4a9e6b}
.qdot.active{background:#e8845a}

/* CHAT */
.chat-wrap{background:#ffffff;border:1px solid #e8e3dc;border-radius:20px;padding:1.5rem}
.panel-label{font-size:0.65rem;font-weight:700;color:#a09890;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1.2rem;display:flex;align-items:center;gap:0.5rem}
.panel-label::before{content:'';width:3px;height:12px;background:#e8845a;border-radius:2px;display:inline-block}
.chat-scroll{max-height:360px;overflow-y:auto;padding-right:0.3rem}
.msg-row{display:flex;gap:0.7rem;margin-bottom:0.9rem;animation:fadein 0.3s ease}
@keyframes fadein{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg-row.user{flex-direction:row-reverse}
.msg-ava{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:0.85rem;flex-shrink:0;background:#f0ede8;border:1px solid #e8e3dc}
.msg-ava.you{background:#fdf0e8;border-color:#f0d0b8}
.mbubble{max-width:78%;padding:0.75rem 1rem;border-radius:12px;font-size:0.85rem;line-height:1.55}
.mbubble.ai{background:#f5f0e8;color:#3d3028;border-top-left-radius:4px;border:1px solid #e8e3dc}
.mbubble.you{background:#fdf0e8;color:#7a3a1a;border-top-right-radius:4px;border:1px solid #f0d0b8}

/* INPUT */
.input-wrap{background:#ffffff;border:1px solid #e8e3dc;border-radius:20px;padding:1.5rem}
.stTextArea textarea{background:#f5f0e8!important;border:1.5px solid #e8e3dc!important;border-radius:10px!important;color:#1a1a1a!important;font-size:0.9rem!important;font-family:'Figtree',sans-serif!important;padding:0.9rem!important;resize:vertical!important}
.stTextArea textarea::placeholder{color:#c0bcb8!important}
.stTextArea textarea:focus{border-color:#e8845a!important;box-shadow:0 0 0 3px rgba(232,132,90,0.15)!important;outline:none!important;background:#ffffff!important}
.stTextArea label{display:none!important}

/* FILE UPLOADER */
[data-testid="stFileUploaderDropzone"]{background:#faf9f6!important;border:2px dashed #ddd8d0!important;border-radius:12px!important}
[data-testid="stFileUploaderDropzoneInstructions"] p{color:#a09890!important}
[data-testid="stFileUploaderDropzone"] svg{stroke:#c0bcb8!important}
[data-testid="stFileUploaderDropzone"]:hover{border-color:#e8845a!important;background:#fdf8f4!important}

/* RESULTS */
.r-banner{background:#1a1a1a;border-radius:20px;padding:3.5rem;text-align:center;margin-bottom:1.5rem;position:relative;overflow:hidden}
.r-banner::before{content:'';position:absolute;top:-120px;left:50%;transform:translateX(-50%);width:700px;height:500px;background:radial-gradient(ellipse,rgba(232,132,90,0.2) 0%,transparent 65%);pointer-events:none}
.verdict-chip{display:inline-flex;align-items:center;padding:0.4rem 1.1rem;border-radius:100px;font-size:0.78rem;font-weight:700;letter-spacing:0.05em;margin-bottom:1.5rem}
.v-hire{background:rgba(74,158,107,0.2);color:#4a9e6b;border:1px solid rgba(74,158,107,0.3)}
.v-maybe{background:rgba(232,132,90,0.2);color:#e8845a;border:1px solid rgba(232,132,90,0.3)}
.v-no{background:rgba(192,64,64,0.2);color:#e07070;border:1px solid rgba(192,64,64,0.3)}
.r-score{font-family:'Fraunces',serif;font-size:6.5rem;font-weight:300;color:#ffffff;line-height:1;letter-spacing:-0.04em}
.r-score span{font-size:2rem;color:#6b6560}
.r-grade{display:inline-block;margin:0.6rem auto;background:rgba(255,255,255,0.08);color:#8a8078;padding:0.3rem 1rem;border-radius:6px;font-size:0.8rem;font-weight:600}
.r-summary{font-size:0.95rem;color:#8a8078;max-width:520px;margin:0.8rem auto 0;line-height:1.65}
.r-card{background:#ffffff;border:1px solid #e8e3dc;border-radius:16px;padding:1.6rem;margin-bottom:1.2rem}
.r-card-title{font-size:0.7rem;font-weight:700;color:#a09890;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:1.2rem}
.bar-track{height:5px;background:#f0ede8;border-radius:6px;overflow:hidden}
.bar-fill{height:100%;border-radius:6px;background:linear-gradient(90deg,#e8845a,#4a9e6b)}
.check-row{font-size:0.87rem;color:#3d3028;padding:0.55rem 0;border-bottom:1px solid #f5f0e8;display:flex;align-items:flex-start;gap:0.6rem}
</style>
""", unsafe_allow_html=True)


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


def render_navbar(show_status=False):
    badge = ""
    if show_status and st.session_state.session_token:
        m = ROUND_META.get(st.session_state.current_round, {})
        badge = f'<span class="nav-badge">{m.get("icon","🎯")} {m.get("label","")}</span>'
    st.markdown(
        f'<div class="navbar">'
        f'<div class="nav-logo"><div class="nav-logo-icon">🎯</div>InterviewAI</div>'
        f'<div class="nav-links">'
        f'<span class="nav-link">How it Works</span>'
        f'<span class="nav-link">Rounds</span>'
        f'<span class="nav-link">Results</span>'
        f'</div>'
        f'<div class="nav-right">{badge}'
        f'<span class="nav-btn-ghost">Groq · llama-3.3-70b</span>'
        f'<span class="nav-btn-solid">Get Started</span>'
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


# ── PAGES ────────────────────────────────────────────────────────────────────
def landing_page():
    render_navbar()
    st.markdown('<div class="page">', unsafe_allow_html=True)

    # HERO
    st.markdown(
        '<div class="hero-section">'
        '<div class="hero-pill"><span class="hero-pill-dot"></span> AI Interviews · Powered by Groq &amp; llama-3.3-70b</div>'
        '<div class="hero-title">Practice Every Round.<br><em>Land Your</em> <strong>Dream Job.</strong></div>'
        '<div class="hero-sub">AI interviewers across HR, Aptitude, Technical and DSA — personalised to your resume, scored in real time.</div>'
        '<div class="hero-stats-row">'
        '<div class="hstat"><div class="hstat-num">4</div><div class="hstat-lbl">Interview Rounds</div></div>'
        '<div class="hstat"><div class="hstat-num">20+</div><div class="hstat-lbl">Questions / Session</div></div>'
        '<div class="hstat"><div class="hstat-num">AI</div><div class="hstat-lbl">Real-time Feedback</div></div>'
        '<div class="hstat"><div class="hstat-num">3×</div><div class="hstat-lbl">Offer Likelihood</div></div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # FEATURE CARDS GRID
    st.markdown(
        '<div class="cards-section">'

        '<div class="feature-card fc-warm">'
        '<div><div class="fc-badge">👤 HR Round</div>'
        '<div class="fc-title">Behavioural &amp;<br>Culture Fit</div>'
        '<div class="fc-sub">Leadership stories, motivation deep-dives, and STAR-method answers — practiced with a real HR persona.</div>'
        '<div class="fc-tags"><span class="fc-tag">STAR Method</span><span class="fc-tag">Culture Fit</span><span class="fc-tag">Leadership</span></div>'
        '</div>'
        '<div class="fc-stat-float"><div class="num">87%</div><div class="lbl">Avg. improvement</div></div>'
        '<div class="fc-emoji">👩‍💼</div>'
        '</div>'

        '<div class="feature-card fc-green">'
        '<div><div class="fc-badge">💻 Technical + 🧮 Aptitude</div>'
        '<div class="fc-title">Deep Tech &amp;<br>Logical Reasoning</div>'
        '<div class="fc-sub">Domain-specific engineering questions, system design, and quantitative reasoning — all in one flow.</div>'
        '<div class="fc-tags"><span class="fc-tag">System Design</span><span class="fc-tag">Quant</span><span class="fc-tag">Data</span></div>'
        '</div>'
        '<div class="fc-stat-float"><div class="num">92%</div><div class="lbl">Topic coverage</div></div>'
        '<div class="fc-emoji">🖥️</div>'
        '</div>'

        '<div class="feature-card fc-dark">'
        '<div><div class="fc-badge">🔢 DSA Round</div>'
        '<div class="fc-title">Algorithms &amp;<br>Data Structures</div>'
        '<div class="fc-sub">Arrays, trees, graphs, dynamic programming — ARIA-9 pushes your problem-solving to the limit.</div>'
        '<div class="fc-tags"><span class="fc-tag">Graphs</span><span class="fc-tag">DP</span><span class="fc-tag">Trees</span><span class="fc-tag">Complexity</span></div>'
        '</div>'
        '<div class="fc-stat-float" style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.1)">'
        '<div class="num" style="color:#e8845a">3×</div><div class="lbl" style="color:#6b6560">More offers</div></div>'
        '<div class="fc-emoji">🤖</div>'
        '</div>'

        '<div class="feature-card fc-purple">'
        '<div><div class="fc-badge">📊 Results &amp; Reports</div>'
        '<div class="fc-title">Detailed Scoring<br>&amp; Feedback</div>'
        '<div class="fc-sub">After every session get a full report: round scores, strengths, improvement areas, and a final hire verdict.</div>'
        '<div class="fc-tags"><span class="fc-tag">Score Report</span><span class="fc-tag">Hire Verdict</span><span class="fc-tag">Tips</span></div>'
        '</div>'
        '<div class="fc-stat-float"><div class="num">A+</div><div class="lbl">Grade breakdown</div></div>'
        '<div class="fc-emoji">📈</div>'
        '</div>'

        '</div>',
        unsafe_allow_html=True
    )

    # FUN FACT
    fact = random.choice(FUN_FACTS)
    st.markdown(
        f'<div class="funfact-bar"><div class="ff-icon">💡</div>'
        f'<div><div class="ff-label">Did You Know?</div>'
        f'<div class="ff-text">{fact}</div></div></div>',
        unsafe_allow_html=True
    )

    # UPLOAD SECTION
    col_left, col_right = st.columns([1, 1], gap="large")

    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown(
        '<div>'
        '<div class="us-title">Upload your resume<br>to begin.</div>'
        '<div class="us-sub">We personalise every question to your experience, skills, and target roles.</div>'
        '<div class="us-points">'
        '<div class="us-point"><div class="us-check">✓</div>Resume-tailored questions</div>'
        '<div class="us-point"><div class="us-check">✓</div>4 complete interview rounds</div>'
        '<div class="us-point"><div class="us-check">✓</div>Real-time AI scoring &amp; feedback</div>'
        '<div class="us-point"><div class="us-check">✓</div>Final hire / no-hire report</div>'
        '</div></div>',
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

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="btn-orange">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)  # upload-section

    st.markdown('</div>', unsafe_allow_html=True)  # page


def interview_page():
    render_navbar(show_status=True)
    render_progress(st.session_state.current_round, st.session_state.rounds_completed)
    st.markdown('<div class="iv-page">', unsafe_allow_html=True)

    rnd = st.session_state.current_round
    iv  = INTERVIEWER_DATA[rnd]
    st.markdown(
        f'<div class="greeter">'
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
            st.markdown('<div class="btn-orange">', unsafe_allow_html=True)
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
                f'<div style="display:flex;justify-content:space-between;font-size:0.85rem;color:#6b6055;margin-bottom:0.4rem">'
                f'<span>{ROUND_META[r]["icon"]} {ROUND_META[r]["label"]}</span>'
                f'<strong style="color:#1a1a1a">{score}/10</strong></div>'
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


# ── Router ────────────────────────────────────────────────────────────────────
if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "interview":
    interview_page()
elif st.session_state.page == "results":
    results_page()

asdkasd
ajjaffinalized UI : left changes size increasing & resolution maintenancefinalized UI : left changes size increasing & resolution maintenance