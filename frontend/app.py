import streamlit as st
import requests
import json
import time
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Interview Simulator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = "http://localhost:8000/api"

ROUND_COLORS = {
    "HR": "#818cf8",
    "APTITUDE": "#fbbf24",
    "TECHNICAL": "#34d399",
    "DSA": "#f87171"
}

ROUND_ICONS = {
    "HR": "👤",
    "APTITUDE": "🧮",
    "TECHNICAL": "💻",
    "DSA": "🔢"
}

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* Global Resets */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Hide Streamlit defaults */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Background */
.stApp {
    background: #0a0a0f;
    color: #e2e8f0;
}

/* Main container */
.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 1400px;
}

/* ─── HERO HEADER ─── */
.hero-header {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a0a2e 50%, #0a1628 100%);
    border: 1px solid rgba(129, 140, 248, 0.2);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(99,102,241,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #a78bfa, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem 0;
    line-height: 1.1;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: #94a3b8;
    margin: 0;
    font-weight: 400;
}

/* ─── CARDS ─── */
.metric-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    transition: border-color 0.2s;
}
.metric-card:hover {
    border-color: #374151;
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    color: #818cf8;
}
.metric-label {
    font-size: 0.78rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}

/* ─── ROUND BADGE ─── */
.round-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 1rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    border: 1px solid;
}

/* ─── CHAT BUBBLES ─── */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem 0;
}
.msg-ai {
    background: linear-gradient(135deg, #1e1b4b, #1a1a2e);
    border: 1px solid rgba(129, 140, 248, 0.25);
    border-radius: 18px 18px 18px 4px;
    padding: 1rem 1.3rem;
    max-width: 85%;
    font-size: 0.95rem;
    line-height: 1.65;
    color: #e2e8f0;
}
.msg-user {
    background: linear-gradient(135deg, #1a2744, #0f2044);
    border: 1px solid rgba(103, 232, 249, 0.2);
    border-radius: 18px 18px 4px 18px;
    padding: 1rem 1.3rem;
    max-width: 85%;
    margin-left: auto;
    font-size: 0.95rem;
    line-height: 1.65;
    color: #e2e8f0;
}
.msg-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    color: #6b7280;
}
.msg-label.ai { color: #818cf8; }
.msg-label.user { color: #67e8f9; text-align: right; }

/* ─── SCORE PANEL ─── */
.score-panel {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}
.score-bar-bg {
    background: #1f2937;
    border-radius: 50px;
    height: 8px;
    overflow: hidden;
    margin-top: 0.5rem;
}
.score-bar-fill {
    height: 100%;
    border-radius: 50px;
    transition: width 0.6s ease;
}

/* ─── FEEDBACK CHIPS ─── */
.chip {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 0.2rem;
}
.chip-green { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.25); }
.chip-red { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }
.chip-blue { background: rgba(129,140,248,0.12); color: #818cf8; border: 1px solid rgba(129,140,248,0.25); }

/* ─── RESUME CARD ─── */
.resume-section {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.resume-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6b7280;
    margin-bottom: 0.5rem;
}

/* ─── UPLOAD ZONE ─── */
.upload-zone {
    border: 2px dashed rgba(129, 140, 248, 0.3);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    background: rgba(129, 140, 248, 0.03);
    transition: all 0.2s;
}
.upload-zone:hover {
    border-color: rgba(129, 140, 248, 0.6);
    background: rgba(129, 140, 248, 0.06);
}

/* ─── PROGRESS STEPS ─── */
.steps-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}
.step {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 0.9rem;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 600;
}
.step.done { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.step.active { background: rgba(129,140,248,0.2); color: #818cf8; border: 1px solid rgba(129,140,248,0.4); }
.step.pending { background: #111827; color: #4b5563; border: 1px solid #1f2937; }
.step-divider { color: #374151; font-size: 0.9rem; }

/* ─── STREAMLIT OVERRIDES ─── */
.stTextArea textarea {
    background: #111827 !important;
    border: 1px solid #374151 !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.9rem 1rem !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 2px rgba(129,140,248,0.15) !important;
}
.stButton button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
}
.stFileUploader {
    background: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="stSidebar"] {
    background: #080810 !important;
    border-right: 1px solid #1f2937 !important;
}
.stAlert {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)


# ─── State Init ────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "home",
        "session_token": None,
        "resume_data": None,
        "resume_score": None,
        "current_round": "HR",
        "chat_history": [],
        "current_question": None,
        "question_number": 1,
        "round_scores": {},
        "last_evaluation": None,
        "interview_complete": False,
        "final_results": None,
        "rounds_done": [],
        "answers_in_round": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

ROUNDS = ["HR", "APTITUDE", "TECHNICAL", "DSA"]
QUESTIONS_PER_ROUND = 3


# ─── API Helpers ───────────────────────────────────────────────────────────────
def api_post(endpoint, data=None, files=None):
    try:
        if files:
            r = requests.post(f"{API_BASE}{endpoint}", files=files, timeout=60)
        else:
            r = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=60)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend. Make sure FastAPI server is running on port 8000.")
        return None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def api_get(endpoint):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend. Make sure FastAPI server is running on port 8000.")
        return None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None


# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.2rem 0 1.5rem 0;">
        <div style="font-size:2.5rem; margin-bottom:0.3rem;">🎯</div>
        <div style="font-size:1.1rem; font-weight:700; color:#818cf8;">AI Interview</div>
        <div style="font-size:0.75rem; color:#4b5563;">Simulator Pro</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    pages = [
        ("🏠", "Home", "home"),
        ("📄", "Resume", "resume"),
        ("🎤", "Interview", "interview"),
        ("📊", "Results", "results"),
    ]

    for icon, label, page_key in pages:
        is_active = st.session_state.page == page_key
        btn_style = "primary" if is_active else "secondary"
        if st.button(f"{icon}  {label}", key=f"nav_{page_key}", use_container_width=True, type=btn_style):
            st.session_state.page = page_key
            st.rerun()

    st.markdown("---")

    # Session info
    if st.session_state.session_token:
        st.markdown(f"""
        <div class="resume-section">
            <div class="resume-section-title">Active Session</div>
            <div style="font-size:0.7rem; color:#818cf8; font-family:'JetBrains Mono'; word-break:break-all;">
                {st.session_state.session_token[:20]}...
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.resume_data:
            name = st.session_state.resume_data.get("name", "Candidate")
            st.markdown(f"""
            <div class="resume-section">
                <div class="resume-section-title">Candidate</div>
                <div style="color:#e2e8f0; font-weight:600;">{name}</div>
            </div>
            """, unsafe_allow_html=True)

        # Round progress
        st.markdown("""
        <div class="resume-section">
            <div class="resume-section-title">Round Progress</div>
        </div>
        """, unsafe_allow_html=True)

        for r in ROUNDS:
            if r in st.session_state.rounds_done:
                score = st.session_state.round_scores.get(r, 0)
                color = ROUND_COLORS[r]
                icon = ROUND_ICONS[r]
                st.markdown(f"""
                <div style="display:flex;align-items:center;justify-content:space-between;
                     padding:0.35rem 0;border-bottom:1px solid #1f2937;">
                    <span style="font-size:0.82rem;">{icon} {r}</span>
                    <span style="color:{color};font-weight:700;font-family:'JetBrains Mono';
                          font-size:0.85rem;">{score:.1f}/10</span>
                </div>
                """, unsafe_allow_html=True)
            elif r == st.session_state.current_round and st.session_state.session_token:
                st.markdown(f"""
                <div style="display:flex;align-items:center;justify-content:space-between;
                     padding:0.35rem 0;border-bottom:1px solid #1f2937;">
                    <span style="font-size:0.82rem;">{ROUND_ICONS[r]} {r}</span>
                    <span style="color:#fbbf24;font-size:0.75rem;">● Active</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex;align-items:center;justify-content:space-between;
                     padding:0.35rem 0;border-bottom:1px solid #1f2937;opacity:0.4;">
                    <span style="font-size:0.82rem;">{ROUND_ICONS[r]} {r}</span>
                    <span style="font-size:0.75rem;color:#4b5563;">Pending</span>
                </div>
                """, unsafe_allow_html=True)

    if st.button("🔄 New Session", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_state()
        st.rerun()

    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0 0;color:#374151;font-size:0.72rem;">
        Powered by Groq + LLaMA 3.3
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE: HOME
# ════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🎯 AI Interview Simulator</div>
        <div class="hero-subtitle">
            Multi-agent powered interview prep — HR, Aptitude, Technical & DSA rounds with real-time scoring
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("4", "Interview Rounds", c1),
        ("12", "Questions Total", c2),
        ("AI", "Powered Scoring", c3),
        ("∞", "Practice Sessions", c4),
    ]
    for val, label, col in stats:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature grid
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="metric-card" style="margin-bottom:1rem;">
            <div style="font-size:1.8rem;margin-bottom:0.6rem;">📄</div>
            <div style="font-weight:700;font-size:1rem;color:#e2e8f0;margin-bottom:0.4rem;">Smart Resume Parser</div>
            <div style="color:#6b7280;font-size:0.88rem;line-height:1.6;">
                Upload PDF/DOCX — AI extracts skills, projects, experience and generates a detailed resume score with improvement tips.
            </div>
        </div>
        <div class="metric-card">
            <div style="font-size:1.8rem;margin-bottom:0.6rem;">🧠</div>
            <div style="font-weight:700;font-size:1rem;color:#e2e8f0;margin-bottom:0.4rem;">Multi-Agent Engine</div>
            <div style="color:#6b7280;font-size:0.88rem;line-height:1.6;">
                Separate AI agents for HR, Aptitude, Technical, and DSA rounds — each tailored to your resume and performance.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card" style="margin-bottom:1rem;">
            <div style="font-size:1.8rem;margin-bottom:0.6rem;">📊</div>
            <div style="font-weight:700;font-size:1rem;color:#e2e8f0;margin-bottom:0.4rem;">Real-time Scoring</div>
            <div style="color:#6b7280;font-size:0.88rem;line-height:1.6;">
                Every answer scored 1-10 with detailed feedback, strengths, improvements, and sample answer hints.
            </div>
        </div>
        <div class="metric-card">
            <div style="font-size:1.8rem;margin-bottom:0.6rem;">🎯</div>
            <div style="font-weight:700;font-size:1rem;color:#e2e8f0;margin-bottom:0.4rem;">Final Analysis</div>
            <div style="color:#6b7280;font-size:0.88rem;line-height:1.6;">
                Comprehensive final report with grade, verdict, round-wise analysis, and personalized next steps.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn = st.columns([1, 2, 1])[1]
    with col_btn:
        if st.button("🚀 Start Interview — Upload Resume", use_container_width=True):
            st.session_state.page = "resume"
            st.rerun()


# ════════════════════════════════════════════════════════════════
# PAGE: RESUME
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "resume":
    st.markdown("""
    <div style="font-size:1.8rem;font-weight:700;color:#e2e8f0;margin-bottom:0.3rem;">
        📄 Resume Upload & Analysis
    </div>
    <div style="color:#6b7280;margin-bottom:1.5rem;">
        Upload your resume to get it parsed and scored before the interview begins
    </div>
    """, unsafe_allow_html=True)

    col_upload, col_preview = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown("""
        <div class="metric-card" style="margin-bottom:1rem;">
            <div style="font-weight:600;color:#818cf8;margin-bottom:0.8rem;">📁 Upload Resume</div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=["pdf", "docx", "doc"],
            help="PDF or DOCX format, max 10MB"
        )

        if uploaded_file:
            st.success(f"✓ {uploaded_file.name} ({uploaded_file.size // 1024} KB)")

            if st.button("🔍 Parse & Score Resume", use_container_width=True):
                with st.spinner("🤖 AI is analyzing your resume..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    result = api_post("/resume/upload", files=files)

                    if result:
                        st.session_state.session_token = result["session_token"]
                        st.session_state.resume_data = result["resume_data"]
                        st.session_state.resume_score = result["resume_score"]
                        st.session_state.page = "resume"
                        st.success("✅ Resume parsed successfully!")
                        st.rerun()

    with col_preview:
        if st.session_state.resume_data:
            rd = st.session_state.resume_data
            rs = st.session_state.resume_score

            st.markdown(f"""
            <div style="font-weight:600;color:#34d399;margin-bottom:1rem;">
                ✅ {rd.get('name', 'Candidate')} — Resume Parsed
            </div>
            """, unsafe_allow_html=True)

            if rs:
                score_pct = rs.get("percentage", 0)
                grade = rs.get("grade", "B")
                color = "#34d399" if score_pct >= 70 else "#fbbf24" if score_pct >= 50 else "#f87171"

                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:1rem;">
                    <div style="display:flex;align-items:center;justify-content:space-between;">
                        <div>
                            <div class="metric-value" style="color:{color};">{score_pct:.0f}%</div>
                            <div class="metric-label">Resume Score</div>
                        </div>
                        <div style="font-size:3rem;font-weight:800;color:{color};">{grade}</div>
                    </div>
                    <div class="score-bar-bg" style="margin-top:1rem;">
                        <div class="score-bar-fill" style="width:{score_pct}%;background:{color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Breakdown
                breakdown = rs.get("breakdown", {})
                breakdown_labels = {
                    "skills": ("Skills", 20),
                    "projects": ("Projects", 25),
                    "experience": ("Experience", 25),
                    "education": ("Education", 15),
                    "contact": ("Contact Info", 10),
                    "certifications": ("Certifications", 5),
                }
                for key, (label, max_pts) in breakdown_labels.items():
                    pts = breakdown.get(key, 0)
                    pct = (pts / max_pts) * 100
                    bar_color = "#34d399" if pct >= 70 else "#fbbf24" if pct >= 40 else "#f87171"
                    st.markdown(f"""
                    <div style="margin-bottom:0.5rem;">
                        <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:3px;">
                            <span style="color:#94a3b8;">{label}</span>
                            <span style="color:{bar_color};font-family:'JetBrains Mono';">{pts}/{max_pts}</span>
                        </div>
                        <div class="score-bar-bg" style="height:5px;">
                            <div class="score-bar-fill" style="width:{pct}%;background:{bar_color};"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # Show resume details
    if st.session_state.resume_data:
        rd = st.session_state.resume_data
        st.markdown("---")

        c1, c2, c3 = st.columns(3)

        with c1:
            skills = rd.get("technical_skills", rd.get("skills", []))
            st.markdown(f"""
            <div class="resume-section">
                <div class="resume-section-title">⚡ Technical Skills ({len(skills)})</div>
                {''.join(f'<span class="chip chip-blue">{s}</span>' for s in skills[:12])}
            </div>
            """, unsafe_allow_html=True)

        with c2:
            projects = rd.get("projects", [])
            proj_html = ""
            for p in projects[:4]:
                name = p.get("name", str(p)) if isinstance(p, dict) else str(p)
                techs = p.get("technologies", []) if isinstance(p, dict) else []
                proj_html += f'<div style="padding:0.4rem 0;border-bottom:1px solid #1f2937;"><div style="font-size:0.85rem;color:#e2e8f0;font-weight:600;">{name}</div>'
                if techs:
                    proj_html += f'<div style="font-size:0.75rem;color:#6b7280;">{", ".join(techs[:3])}</div>'
                proj_html += "</div>"
            st.markdown(f"""
            <div class="resume-section">
                <div class="resume-section-title">🔨 Projects ({len(projects)})</div>
                {proj_html if proj_html else '<span style="color:#4b5563;font-size:0.82rem;">No projects found</span>'}
            </div>
            """, unsafe_allow_html=True)

        with c3:
            exp = rd.get("experience", [])
            exp_html = ""
            for e in exp[:3]:
                if isinstance(e, dict):
                    role = e.get("role", "")
                    company = e.get("company", "")
                    dur = e.get("duration", "")
                    exp_html += f'<div style="padding:0.4rem 0;border-bottom:1px solid #1f2937;"><div style="font-size:0.85rem;color:#e2e8f0;font-weight:600;">{role}</div><div style="font-size:0.75rem;color:#6b7280;">{company} · {dur}</div></div>'
                else:
                    exp_html += f'<div style="font-size:0.82rem;color:#e2e8f0;padding:0.3rem 0;">{str(e)}</div>'
            st.markdown(f"""
            <div class="resume-section">
                <div class="resume-section-title">💼 Experience ({len(exp)})</div>
                {exp_html if exp_html else '<span style="color:#4b5563;font-size:0.82rem;">No experience listed</span>'}
            </div>
            """, unsafe_allow_html=True)

        # Feedback chips
        if st.session_state.resume_score:
            feedback = st.session_state.resume_score.get("feedback", [])
            if feedback:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.6rem;">💡 Resume Feedback</div>
                """, unsafe_allow_html=True)
                chips_html = ""
                for i, f in enumerate(feedback):
                    chip_cls = "chip-green" if i % 3 != 2 else "chip-red"
                    chips_html += f'<span class="chip {chip_cls}">{f}</span> '
                st.markdown(chips_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_cta = st.columns([1, 2, 1])[1]
        with col_cta:
            if st.button("🎤 Start Interview Now →", use_container_width=True):
                st.session_state.page = "interview"
                st.rerun()
    else:
        st.markdown("""
        <div class="upload-zone" style="margin-top:2rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">📄</div>
            <div style="font-size:1.1rem;font-weight:600;color:#e2e8f0;margin-bottom:0.5rem;">
                Upload your resume to begin
            </div>
            <div style="color:#6b7280;font-size:0.9rem;">
                Supports PDF and DOCX • AI-powered extraction
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE: INTERVIEW
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "interview":
    if not st.session_state.session_token:
        st.warning("⚠️ Please upload your resume first!")
        if st.button("Go to Resume Upload"):
            st.session_state.page = "resume"
            st.rerun()
    elif st.session_state.interview_complete:
        st.markdown("""
        <div style="text-align:center;padding:3rem;">
            <div style="font-size:4rem;margin-bottom:1rem;">🎉</div>
            <div style="font-size:2rem;font-weight:700;color:#34d399;margin-bottom:0.5rem;">
                Interview Complete!
            </div>
            <div style="color:#94a3b8;font-size:1rem;">All rounds finished. Check your results!</div>
        </div>
        """, unsafe_allow_html=True)
        col = st.columns([1, 2, 1])[1]
        with col:
            if st.button("📊 View Full Results →", use_container_width=True):
                st.session_state.page = "results"
                st.rerun()
    else:
        # ── Round Progress Bar ──
        steps_html = '<div class="steps-row">'
        for i, r in enumerate(ROUNDS):
            if r in st.session_state.rounds_done:
                steps_html += f'<div class="step done">✓ {r}</div>'
            elif r == st.session_state.current_round:
                steps_html += f'<div class="step active">● {r}</div>'
            else:
                steps_html += f'<div class="step pending">{r}</div>'
            if i < len(ROUNDS) - 1:
                steps_html += '<div class="step-divider">›</div>'
        steps_html += "</div>"
        st.markdown(steps_html, unsafe_allow_html=True)

        # ── Main Interview Area ──
        col_chat, col_score = st.columns([3, 1], gap="large")

        with col_chat:
            current_round = st.session_state.current_round
            r_color = ROUND_COLORS.get(current_round, "#818cf8")
            r_icon = ROUND_ICONS.get(current_round, "🎤")

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:1.2rem;">
                <div style="font-size:1.8rem;">{r_icon}</div>
                <div>
                    <div style="font-size:1.2rem;font-weight:700;color:{r_color};">{current_round} Round</div>
                    <div style="color:#6b7280;font-size:0.82rem;">
                        Question {min(st.session_state.question_number, QUESTIONS_PER_ROUND)} of {QUESTIONS_PER_ROUND}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Start round if no question yet
            if not st.session_state.current_question:
                with st.spinner(f"🤖 {current_round} agent is preparing your first question..."):
                    result = api_post("/interview/start", {
                        "session_token": st.session_state.session_token,
                        "round_name": current_round
                    })
                    if result:
                        st.session_state.current_question = result["question"]
                        st.session_state.question_number = result.get("question_number", 1)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": result["question"],
                            "round": current_round
                        })
                        st.rerun()

            # Chat display
            if st.session_state.chat_history:
                chat_html = '<div class="chat-container">'
                for msg in st.session_state.chat_history:
                    if msg["role"] == "assistant":
                        chat_html += f"""
                        <div>
                            <div class="msg-label ai">🤖 AI Interviewer</div>
                            <div class="msg-ai">{msg['content']}</div>
                        </div>"""
                    else:
                        chat_html += f"""
                        <div style="display:flex;flex-direction:column;align-items:flex-end;">
                            <div class="msg-label user">You 👤</div>
                            <div class="msg-user">{msg['content']}</div>
                        </div>"""
                chat_html += "</div>"
                st.markdown(chat_html, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Answer input
            if st.session_state.current_question:
                answer = st.text_area(
                    "Your Answer",
                    placeholder="Type your answer here... Be as detailed as possible.",
                    height=130,
                    key=f"ans_{current_round}_{st.session_state.question_number}"
                )

                btn_col1, btn_col2 = st.columns([3, 1])
                with btn_col1:
                    if st.button("📤 Submit Answer", use_container_width=True):
                        if not answer or len(answer.strip()) < 3:
                            st.warning("Please write an answer before submitting")
                        else:
                            with st.spinner("🤖 Evaluating your answer..."):
                                result = api_post("/interview/answer", {
                                    "session_token": st.session_state.session_token,
                                    "answer": answer,
                                    "question": st.session_state.current_question,
                                    "round_name": current_round
                                })

                                if result:
                                    # Add to history
                                    st.session_state.chat_history.append({
                                        "role": "user", "content": answer, "round": current_round
                                    })

                                    st.session_state.last_evaluation = result.get("evaluation")
                                    st.session_state.answers_in_round = result.get("answered_in_round", 1)

                                    if result.get("is_interview_complete"):
                                        st.session_state.interview_complete = True
                                        st.rerun()
                                    elif result.get("is_round_complete"):
                                        completed_round = current_round
                                        eval_data = result.get("evaluation", {})
                                        # Update scores from history
                                        if completed_round not in st.session_state.rounds_done:
                                            st.session_state.rounds_done.append(completed_round)

                                        next_r = result.get("next_round")
                                        if next_r:
                                            st.session_state.current_round = next_r
                                            st.session_state.current_question = None
                                            st.session_state.question_number = 1
                                            st.session_state.chat_history = []
                                        st.rerun()
                                    else:
                                        next_q = result.get("next_question")
                                        if next_q:
                                            st.session_state.current_question = next_q
                                            st.session_state.question_number += 1
                                            st.session_state.chat_history.append({
                                                "role": "assistant", "content": next_q, "round": current_round
                                            })
                                        st.rerun()

                with btn_col2:
                    if st.button("⏭️ Skip", use_container_width=True):
                        with st.spinner("Skipping..."):
                            result = api_post("/interview/answer", {
                                "session_token": st.session_state.session_token,
                                "answer": "[Skipped]",
                                "question": st.session_state.current_question,
                                "round_name": current_round
                            })
                            if result:
                                if result.get("is_interview_complete"):
                                    st.session_state.interview_complete = True
                                elif result.get("is_round_complete"):
                                    if current_round not in st.session_state.rounds_done:
                                        st.session_state.rounds_done.append(current_round)
                                    next_r = result.get("next_round")
                                    if next_r:
                                        st.session_state.current_round = next_r
                                        st.session_state.current_question = None
                                        st.session_state.question_number = 1
                                        st.session_state.chat_history = []
                                else:
                                    next_q = result.get("next_question")
                                    if next_q:
                                        st.session_state.current_question = next_q
                                        st.session_state.question_number += 1
                                        st.session_state.chat_history.append({
                                            "role": "assistant", "content": next_q, "round": current_round
                                        })
                                st.rerun()

        # ── Right Panel: Live Scoring ──
        with col_score:
            st.markdown("""
            <div style="font-weight:600;color:#e2e8f0;margin-bottom:1rem;font-size:0.9rem;">
                📊 Live Scores
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.last_evaluation:
                ev = st.session_state.last_evaluation
                score = ev.get("score", 0)
                score_color = "#34d399" if score >= 7 else "#fbbf24" if score >= 5 else "#f87171"

                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:1rem;text-align:center;">
                    <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3rem;">Last Answer</div>
                    <div style="font-size:2.5rem;font-weight:800;color:{score_color};font-family:'JetBrains Mono';">{score}/10</div>
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width:{score*10}%;background:{score_color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                feedback = ev.get("feedback", "")
                if feedback:
                    st.markdown(f"""
                    <div class="metric-card" style="margin-bottom:0.8rem;">
                        <div style="font-size:0.7rem;color:#818cf8;font-weight:700;margin-bottom:0.4rem;">FEEDBACK</div>
                        <div style="font-size:0.82rem;color:#94a3b8;line-height:1.6;">{feedback}</div>
                    </div>
                    """, unsafe_allow_html=True)

                strengths = ev.get("strengths", [])
                if strengths:
                    st.markdown(f"""
                    <div class="metric-card" style="margin-bottom:0.8rem;">
                        <div style="font-size:0.7rem;color:#34d399;font-weight:700;margin-bottom:0.4rem;">✓ STRENGTHS</div>
                        {''.join(f'<div style="font-size:0.8rem;color:#94a3b8;padding:0.2rem 0;">• {s}</div>' for s in strengths)}
                    </div>
                    """, unsafe_allow_html=True)

                improvements = ev.get("improvements", [])
                if improvements:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size:0.7rem;color:#fbbf24;font-weight:700;margin-bottom:0.4rem;">↑ IMPROVE</div>
                        {''.join(f'<div style="font-size:0.8rem;color:#94a3b8;padding:0.2rem 0;">• {imp}</div>' for imp in improvements)}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card" style="text-align:center;padding:2rem 1rem;">
                    <div style="font-size:2rem;margin-bottom:0.5rem;">⏳</div>
                    <div style="color:#4b5563;font-size:0.85rem;">Submit an answer to<br>see your score</div>
                </div>
                """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE: RESULTS
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "results":
    if not st.session_state.session_token:
        st.warning("⚠️ No session found. Please start an interview first.")
    else:
        with st.spinner("Loading results..."):
            results = api_get(f"/evaluation/results/{st.session_state.session_token}")

        if not results:
            st.error("Could not load results")
        else:
            final = results.get("final_feedback", {})
            overall = results.get("overall_score", 0)
            round_scores = results.get("round_scores", {})
            round_details = results.get("round_details", {})

            # ── Hero ──
            grade = final.get("grade", "B") if final else "B"
            verdict = final.get("verdict", "Recommended") if final else "—"
            verdict_color = "#34d399" if "Recommend" in verdict else "#fbbf24" if "Maybe" in verdict else "#f87171"
            score_color = "#34d399" if overall >= 7 else "#fbbf24" if overall >= 5 else "#f87171"

            st.markdown(f"""
            <div class="hero-header">
                <div style="display:flex;align-items:center;justify-content:space-between;">
                    <div>
                        <div style="font-size:0.8rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">
                            Interview Complete
                        </div>
                        <div class="hero-title" style="font-size:2rem;">📊 Performance Report</div>
                        {f'<div style="color:#94a3b8;margin-top:0.5rem;">{final.get("executive_summary", "")}</div>' if final else ''}
                    </div>
                    <div style="text-align:center;min-width:160px;">
                        <div style="font-size:4rem;font-weight:800;color:{score_color};font-family:'JetBrains Mono';">{overall:.1f}</div>
                        <div style="color:#6b7280;font-size:0.8rem;">Overall Score / 10</div>
                        <div style="margin-top:0.5rem;">
                            <span style="font-size:2rem;font-weight:800;color:{score_color};">{grade}</span>
                            <span style="margin-left:0.8rem;padding:0.2rem 0.8rem;background:rgba(52,211,153,0.15);
                                  color:{verdict_color};border-radius:50px;font-size:0.78rem;font-weight:600;">
                                {verdict}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Round Score Cards ──
            cols = st.columns(4)
            for i, r in enumerate(ROUNDS):
                score = round_scores.get(r, 0)
                color = ROUND_COLORS.get(r, "#818cf8")
                icon = ROUND_ICONS.get(r, "🎤")
                pct = (score / 10) * 100
                with cols[i]:
                    st.markdown(f"""
                    <div class="metric-card" style="border-color:{color}33;">
                        <div style="font-size:1.4rem;">{icon}</div>
                        <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;margin:0.3rem 0;">{r}</div>
                        <div style="font-size:2rem;font-weight:800;color:{color};font-family:'JetBrains Mono';">{score:.1f}</div>
                        <div class="score-bar-bg">
                            <div class="score-bar-fill" style="width:{pct}%;background:{color};"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Plotly Radar Chart ──
            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                if round_scores:
                    categories = list(round_scores.keys())
                    values = list(round_scores.values())
                    values_closed = values + [values[0]]
                    categories_closed = categories + [categories[0]]

                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=values_closed,
                        theta=categories_closed,
                        fill='toself',
                        fillcolor='rgba(99,102,241,0.15)',
                        line=dict(color='#818cf8', width=2),
                        marker=dict(size=8, color='#818cf8'),
                        name='Your Score'
                    ))
                    fig.add_trace(go.Scatterpolar(
                        r=[10, 10, 10, 10, 10],
                        theta=categories_closed,
                        fill='toself',
                        fillcolor='rgba(255,255,255,0.02)',
                        line=dict(color='#374151', width=1, dash='dot'),
                        name='Max Score'
                    ))
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 10], tickfont=dict(color='#6b7280', size=10), gridcolor='#1f2937'),
                            angularaxis=dict(tickfont=dict(color='#94a3b8', size=12), gridcolor='#1f2937'),
                            bgcolor='#0a0a0f'
                        ),
                        showlegend=True,
                        legend=dict(font=dict(color='#94a3b8')),
                        paper_bgcolor='#111827',
                        plot_bgcolor='#111827',
                        margin=dict(t=30, b=30, l=30, r=30),
                        height=320,
                        title=dict(text="Performance Radar", font=dict(color='#e2e8f0', size=14))
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with col_chart2:
                if round_scores:
                    rounds_list = list(round_scores.keys())
                    scores_list = list(round_scores.values())
                    colors_list = [ROUND_COLORS.get(r, "#818cf8") for r in rounds_list]

                    fig2 = go.Figure(go.Bar(
                        x=rounds_list,
                        y=scores_list,
                        marker_color=colors_list,
                        text=[f"{s:.1f}" for s in scores_list],
                        textposition='inside',
                        textfont=dict(color='white', size=14, family='JetBrains Mono'),
                    ))
                    fig2.add_hline(y=7, line_dash="dot", line_color="#34d399", annotation_text="Good (7)", annotation_font_color="#34d399")
                    fig2.update_layout(
                        paper_bgcolor='#111827',
                        plot_bgcolor='#111827',
                        xaxis=dict(tickfont=dict(color='#94a3b8'), gridcolor='#1f2937'),
                        yaxis=dict(range=[0, 10], tickfont=dict(color='#94a3b8'), gridcolor='#1f2937'),
                        height=320,
                        title=dict(text="Round-wise Scores", font=dict(color='#e2e8f0', size=14)),
                        margin=dict(t=40, b=20, l=20, r=20),
                        showlegend=False
                    )
                    st.plotly_chart(fig2, use_container_width=True)

            # ── Final Feedback ──
            if final:
                st.markdown("---")
                col_str, col_imp = st.columns(2)

                with col_str:
                    strengths = final.get("top_strengths", [])
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-weight:700;color:#34d399;margin-bottom:0.8rem;">💪 Top Strengths</div>
                        {''.join(f'<div style="display:flex;gap:0.5rem;padding:0.35rem 0;border-bottom:1px solid #1f2937;"><span style="color:#34d399;">✓</span><span style="font-size:0.88rem;color:#94a3b8;">{s}</span></div>' for s in strengths)}
                    </div>
                    """, unsafe_allow_html=True)

                with col_imp:
                    improvements = final.get("key_improvements", [])
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-weight:700;color:#fbbf24;margin-bottom:0.8rem;">📈 Key Improvements</div>
                        {''.join(f'<div style="display:flex;gap:0.5rem;padding:0.35rem 0;border-bottom:1px solid #1f2937;"><span style="color:#fbbf24;">→</span><span style="font-size:0.88rem;color:#94a3b8;">{imp}</span></div>' for imp in improvements)}
                    </div>
                    """, unsafe_allow_html=True)

                # Next steps
                next_steps = final.get("next_steps", [])
                if next_steps:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-weight:700;color:#818cf8;margin-bottom:0.8rem;">🚀 Your Next Steps</div>
                        <div style="display:flex;flex-wrap:wrap;gap:0.5rem;">
                            {''.join(f'<span class="chip chip-blue">{step}</span>' for step in next_steps)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Per-Round Q&A Review ──
            st.markdown("---")
            st.markdown("""
            <div style="font-size:1.1rem;font-weight:700;color:#e2e8f0;margin-bottom:1rem;">
                🗂️ Detailed Round Review
            </div>
            """, unsafe_allow_html=True)

            for round_name, details in round_details.items():
                with st.expander(f"{ROUND_ICONS.get(round_name,'🎤')} {round_name} Round — Score: {details.get('score', 0):.1f}/10"):
                    for i, qa in enumerate(details.get("questions", [])):
                        score = qa.get("score", 0)
                        s_color = "#34d399" if score >= 7 else "#fbbf24" if score >= 5 else "#f87171"
                        st.markdown(f"""
                        <div class="metric-card" style="margin-bottom:0.8rem;">
                            <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:0.6rem;">
                                <div style="font-weight:600;color:#818cf8;font-size:0.85rem;">Q{i+1}</div>
                                <span style="color:{s_color};font-weight:700;font-family:'JetBrains Mono';">{score}/10</span>
                            </div>
                            <div style="font-size:0.88rem;color:#e2e8f0;margin-bottom:0.5rem;">{qa.get('question', '')}</div>
                            <div style="font-size:0.82rem;color:#6b7280;padding:0.5rem;background:#0a0a0f;border-radius:8px;margin-bottom:0.5rem;">
                                Your answer: {qa.get('answer', '')[:300]}
                            </div>
                            <div style="font-size:0.82rem;color:#94a3b8;font-style:italic;">
                                📝 {qa.get('feedback', '')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col_restart = st.columns([1, 2, 1])[1]
            with col_restart:
                if st.button("🔄 Start New Interview", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    init_state()
                    st.rerun()
