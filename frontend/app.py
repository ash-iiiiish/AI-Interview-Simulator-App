"""
app.py — Streamlit frontend for AI Interview Simulator.

Run:
    streamlit run frontend/app.py
"""

import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load .env so BACKEND_URL is available
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
ROUNDS = ["HR", "TECHNICAL", "DSA"]
ROUND_ICONS = {"HR": "👤", "TECHNICAL": "💻", "DSA": "🔢"}
ROUND_COLORS = {"HR": "#6366f1", "TECHNICAL": "#10b981", "DSA": "#ef4444"}

# ── Page Config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Interview Simulator",
    page_icon="🎯",
    layout="wide",
)

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1e293b; }
    .subtitle   { color: #64748b; font-size: 1rem; margin-bottom: 1.5rem; }
    .round-badge {
        display: inline-block; padding: 4px 14px;
        border-radius: 999px; font-weight: 600; font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }
    .score-card {
        background: #f8fafc; border: 1px solid #e2e8f0;
        border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 1rem;
    }
    .chat-q { background: #f1f5f9; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 0.5rem; }
    .chat-a { background: #e0f2fe; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Session State Init ────────────────────────────────────────────────────────

for key, default in {
    "page": "home",
    "session_token": None,
    "resume_data": None,
    "current_round": "HR",
    "current_question": None,
    "question_number": 1,
    "round_complete": False,
    "interview_complete": False,
    "chat_history": [],   # list of {"role", "content"}
    "last_eval": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Helper ────────────────────────────────────────────────────────────────────

def api(method: str, path: str, **kwargs):
    """Make an API call; return (data, error_msg)."""
    try:
        resp = getattr(requests, method)(f"{BACKEND_URL}{path}", **kwargs)
        if resp.ok:
            return resp.json(), None
        return None, resp.json().get("detail", "API error")
    except requests.ConnectionError:
        return None, "Cannot connect to the backend. Is it running?"
    except Exception as e:
        return None, str(e)


def score_color(score: float) -> str:
    if score >= 8:   return "#10b981"
    if score >= 6:   return "#f59e0b"
    return "#ef4444"


# ── Pages ─────────────────────────────────────────────────────────────────────

def page_home():
    st.markdown('<div class="main-title">🎯 AI Interview Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Upload your resume and practice with an AI interviewer — powered by Groq (free)</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("📄 Upload Your Resume")
        st.caption("Supported formats: PDF, DOCX")
        uploaded = st.file_uploader("Choose your resume", type=["pdf", "docx", "doc"], label_visibility="collapsed")

        if uploaded:
            if st.button("🚀 Start Interview", use_container_width=True, type="primary"):
                with st.spinner("Parsing your resume with AI..."):
                    data, err = api(
                        "post",
                        "/api/resume/upload",
                        files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
                        timeout=120,
                    )
                if err:
                    st.error(f"❌ {err}")
                else:
                    st.session_state.session_token = data["session_token"]
                    st.session_state.resume_data   = data["resume_data"]
                    st.session_state.current_round  = "HR"
                    st.session_state.page           = "interview"
                    st.rerun()

    with col2:
        st.subheader("📋 How it works")
        st.markdown("""
1. **Upload** your PDF or DOCX resume
2. **AI parses** your skills, projects, and experience
3. **Answer questions** across 3 rounds: HR → Technical → DSA
4. **Get scored** on each answer with detailed feedback
5. **View your report** with strengths and improvement tips
        """)

        st.subheader("🔢 Interview Rounds")
        for r in ROUNDS:
            color = ROUND_COLORS[r]
            icon  = ROUND_ICONS[r]
            st.markdown(
                f'<span class="round-badge" style="background:{color}22;color:{color}">'
                f'{icon} {r}</span>',
                unsafe_allow_html=True,
            )


def page_interview():
    resume = st.session_state.resume_data or {}
    round_name = st.session_state.current_round

    # Sidebar — candidate info
    with st.sidebar:
        st.markdown("### 👤 Candidate")
        st.write(f"**{resume.get('name', 'Candidate')}**")
        skills = resume.get("technical_skills") or resume.get("skills") or []
        if skills:
            st.caption("Skills: " + ", ".join(skills[:6]))

        st.markdown("---")
        st.markdown("### 📊 Progress")
        for r in ROUNDS:
            icon = ROUND_ICONS[r]
            if r == round_name:
                st.markdown(f"▶️ **{icon} {r}** ← current")
            elif ROUNDS.index(r) < ROUNDS.index(round_name):
                st.markdown(f"✅ {icon} {r}")
            else:
                st.markdown(f"⏳ {icon} {r}")

        st.markdown("---")
        if st.button("🏠 Exit Interview", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    # Main area
    color = ROUND_COLORS[round_name]
    icon  = ROUND_ICONS[round_name]
    st.markdown(
        f'<span class="round-badge" style="background:{color}22;color:{color};font-size:1rem">'
        f'{icon} {round_name} Round</span>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**Question {st.session_state.question_number} of 3**")
    st.markdown("---")

    # Load first question if not loaded
    if not st.session_state.current_question:
        with st.spinner(f"Starting {round_name} round..."):
            data, err = api(
                "post", "/api/interview/start",
                json={"session_token": st.session_state.session_token, "round_name": round_name},
                timeout=120,
            )
        if err:
            st.error(f"❌ {err}")
            return
        st.session_state.current_question  = data["question"]
        st.session_state.question_number   = data["question_number"]
        st.session_state.round_complete    = False
        st.rerun()

    # Chat history display
    for msg in st.session_state.chat_history:
        if msg["role"] == "assistant":
            st.markdown(f'<div class="chat-q">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-a">👤 {msg["content"]}</div>', unsafe_allow_html=True)

    # Show current question
    if st.session_state.current_question and not st.session_state.round_complete:
        st.markdown(f'<div class="chat-q">🤖 {st.session_state.current_question}</div>', unsafe_allow_html=True)

        # Show last evaluation (non-blocking)
        if st.session_state.last_eval:
            ev = st.session_state.last_eval
            score = ev.get("score", 0)
            with st.expander(f"📊 Last answer scored: {score}/10", expanded=False):
                st.write(ev.get("feedback", ""))
                c1, c2 = st.columns(2)
                with c1:
                    if ev.get("strengths"):
                        st.write("✅ **Strengths:**")
                        for s in ev["strengths"]:
                            st.write(f"- {s}")
                with c2:
                    if ev.get("improvements"):
                        st.write("🔧 **Improvements:**")
                        for i in ev["improvements"]:
                            st.write(f"- {i}")
            st.session_state.last_eval = None

        answer = st.text_area("Your answer:", height=120, placeholder="Type your answer here...", key=f"ans_{st.session_state.question_number}")

        if st.button("✅ Submit Answer", type="primary", use_container_width=True):
            if not answer.strip():
                st.warning("Please write an answer before submitting.")
            else:
                with st.spinner("Evaluating your answer..."):
                    data, err = api(
                        "post", "/api/interview/answer",
                        json={
                            "session_token": st.session_state.session_token,
                            "answer": answer,
                            "question": st.session_state.current_question,
                            "round_name": round_name,
                        },
                        timeout=120,
                    )
                if err:
                    st.error(f"❌ {err}")
                    return

                # Update chat history
                st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.current_question})
                st.session_state.chat_history.append({"role": "user", "content": answer})
                st.session_state.last_eval = data["evaluation"]

                if data["is_interview_complete"]:
                    st.session_state.interview_complete = True
                    st.session_state.current_question = None
                    st.session_state.page = "results"
                    st.rerun()
                elif data["is_round_complete"] and data["next_round"]:
                    st.session_state.current_round    = data["next_round"]
                    st.session_state.current_question = None
                    st.session_state.question_number  = 1
                    st.session_state.chat_history     = []
                    st.session_state.round_complete   = False
                    st.rerun()
                else:
                    st.session_state.current_question = data["next_question"]
                    st.session_state.question_number += 1
                    st.rerun()

    elif st.session_state.round_complete:
        st.success(f"✅ {round_name} Round Complete!")


def page_results():
    st.markdown('<div class="main-title">📊 Interview Results</div>', unsafe_allow_html=True)

    with st.spinner("Generating your performance report..."):
        data, err = api("get", f"/api/evaluation/results/{st.session_state.session_token}", timeout=120)

    if err:
        st.error(f"❌ {err}")
        return

    overall = data.get("overall_score", 0)
    round_scores = data.get("round_scores", {})
    report = data.get("final_report", {})

    # Overall score
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Score", f"{overall:.1f}/10")
    col2.metric("Grade", report.get("grade", "N/A"))
    col3.metric("Verdict", report.get("verdict", "N/A"))

    st.markdown("---")

    # Round scores
    st.subheader("📋 Round Breakdown")
    rcols = st.columns(len(round_scores))
    for i, (r, score) in enumerate(round_scores.items()):
        icon = ROUND_ICONS.get(r, "📌")
        rcols[i].metric(f"{icon} {r}", f"{score:.1f}/10")

    # Summary
    if report.get("summary"):
        st.markdown("---")
        st.subheader("📝 Summary")
        st.write(report["summary"])

    # Strengths & Improvements
    if report.get("top_strengths") or report.get("improvements"):
        col1, col2 = st.columns(2)
        with col1:
            if report.get("top_strengths"):
                st.subheader("✅ Top Strengths")
                for s in report["top_strengths"]:
                    st.write(f"- {s}")
        with col2:
            if report.get("improvements"):
                st.subheader("🔧 Areas to Improve")
                for i in report["improvements"]:
                    st.write(f"- {i}")

    # Next Steps
    if report.get("next_steps"):
        st.subheader("🚀 Next Steps")
        for step in report["next_steps"]:
            st.write(f"- {step}")

    # Q&A Review
    st.markdown("---")
    st.subheader("📖 Q&A Review")
    round_details = data.get("round_details", {})
    for round_name, detail in round_details.items():
        icon = ROUND_ICONS.get(round_name, "📌")
        with st.expander(f"{icon} {round_name} Round — {detail['score']:.1f}/10"):
            for i, qa in enumerate(detail.get("questions", []), 1):
                st.markdown(f"**Q{i}:** {qa['question']}")
                st.markdown(f"**Your answer:** {qa['answer']}")
                st.markdown(f"**Score:** {qa.get('score', 0):.1f}/10  |  **Feedback:** {qa.get('feedback', '')}")
                st.markdown("---")

    st.markdown("---")
    if st.button("🔄 Start New Interview", type="primary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ── Router ────────────────────────────────────────────────────────────────────

page = st.session_state.page

if page == "home":
    page_home()
elif page == "interview":
    page_interview()
elif page == "results":
    page_results()
