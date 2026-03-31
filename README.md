# 🎯 AI Interview Simulator

A full-stack AI-powered interview simulator with a cinematic UI.  
Practice across **4 rounds** — HR, Aptitude, Technical & DSA — with real-time AI scoring powered by **Groq (Llama 3.3-70B)**.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 AI Interviewers | 4 distinct AI personas for each round |
| 📄 Resume Parsing | PDF & DOCX support via pdfplumber + python-docx |
| 🧠 Smart Questions | Personalized to your resume skills & projects |
| 📊 Live Scoring | Per-answer scores with strengths & improvements |
| 🗄️ PostgreSQL | Full session persistence across rounds |
| 🎨 Cinematic UI | Sci-fi HUD, holographic avatar, animated EQ bars |

---

## 🗂 Project Structure

```
AI-Interview-Simulator/
├── backend/
│   ├── main.py                     ← FastAPI entry point
│   └── app/
│       ├── agents/llm_agents.py    ← All Groq LLM logic
│       ├── core/
│       │   ├── config.py           ← pydantic-settings config
│       │   └── database.py         ← SQLAlchemy 2.x engine
│       ├── models/models.py        ← ORM tables
│       ├── routers/                ← API endpoints
│       │   ├── interview.py
│       │   ├── resume.py
│       │   ├── evaluation.py
│       │   └── sessions.py
│       ├── schemas/schemas.py      ← Pydantic v2 request/response
│       └── services/resume_service.py
├── frontend/
│   ├── app.py                      ← Streamlit UI (cinematic)
│   └── .streamlit/config.toml
├── requirements.txt                ← Single clean file, Python 3.12+
└── .env.example                    ← Copy to .env and fill in keys
```

---

## ⚙️ Setup

### 1. Clone & Install

```bash
git clone <your-repo>
cd AI-Interview-Simulator

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Then edit .env with your values:
#   GROQ_API_KEY=gsk_...
#   DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_interview_db
```

Get a free Groq API key at: https://console.groq.com

### 3. Set Up PostgreSQL

```bash
# Ubuntu / Debian
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

# Create database
sudo -u postgres psql -c "CREATE DATABASE ai_interview_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ai_interview_db TO postgres;"
```

> Tables are auto-created on first backend startup via SQLAlchemy.

### 4. Run the Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Verify: http://localhost:8000/docs

### 5. Run the Frontend

```bash
cd frontend
streamlit run app.py
```

Open: http://localhost:8501

---

## 🐘 PostgreSQL Schema

Tables created automatically:

| Table | Purpose |
|---|---|
| `interview_sessions` | Session token, resume data, current round |
| `round_results` | Per-round scores and completion status |
| `question_answers` | Every Q&A pair with individual scores |
| `chat_messages` | Full conversation log per round |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/resume/upload` | Upload PDF/DOCX, parse, create session |
| GET  | `/api/resume/score/{token}` | Get resume score |
| POST | `/api/interview/start` | Start/resume a round, get first question |
| POST | `/api/interview/answer` | Submit answer, get evaluation + next Q |
| GET  | `/api/interview/history/{token}` | Get chat history |
| GET  | `/api/evaluation/results/{token}` | Full performance report |
| GET  | `/api/sessions/{token}` | Session status |
| DELETE | `/api/sessions/{token}` | Delete session |

---

## 🐛 Bug Fixes Applied (vs Original)

| File | Fix |
|---|---|
| `requirements.txt` | Removed duplicates; updated to latest Python 3.12-compatible versions; added `pydantic-settings` |
| `core/config.py` | Replaced bare `os.getenv()` with `pydantic-settings BaseSettings` |
| `core/database.py` | Fixed deprecated `declarative_base()` → `class Base(DeclarativeBase)` (SQLAlchemy 2.x) |
| `schemas/schemas.py` | Updated to Python 3.12 native `list[str]` / `dict[str,Any]` typing |
| `llm_agents.py` | Fixed `None` dict access errors with safe `or []` fallbacks |
| `resume_service.py` | Same null-safety fixes; added `pool_pre_ping` to engine |
| `frontend/app.py` | Complete UI overhaul with cinematic wallpaper, holographic avatar, animated HUD |

---

## 🚀 Docker (Optional)

```bash
docker-compose up --build
```

This starts both backend (port 8000) and frontend (port 8501) with a PostgreSQL container.
