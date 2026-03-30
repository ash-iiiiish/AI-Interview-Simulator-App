# 🎯 AI Interview Simulator

A production-grade, multi-agent AI-powered interview simulator built with **FastAPI**, **Streamlit**, **Groq (LLaMA 3.3)**, and **PostgreSQL**.

---

## 🏗️ Architecture

```
ai-interview-simulator/
├── backend/                   # FastAPI backend
│   ├── main.py                # App entry point
│   ├── database.py            # PostgreSQL connection
│   ├── models.py              # SQLAlchemy ORM models
│   ├── init_db.py             # DB initialization script
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── routers/
│   │   ├── resume.py          # /api/resume/* endpoints
│   │   ├── interview.py       # /api/interview/* endpoints
│   │   ├── evaluation.py      # /api/evaluation/* endpoints
│   │   └── sessions.py        # /api/sessions/* endpoints
│   └── services/
│       ├── resume_service.py  # PDF parsing + LLM extraction
│       └── interview_service.py # Multi-agent interview logic
│
├── frontend/                  # Streamlit frontend
│   ├── app.py                 # Main Streamlit app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .streamlit/
│       └── config.toml        # Dark theme config
│
├── docker-compose.yml         # One-command deployment
├── .env.example               # Environment variables template
└── README.md
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 📄 **Resume Parser** | PDF/DOCX → structured JSON via LLM |
| 📊 **Resume Scorer** | 6-dimension scoring with feedback |
| 🤖 **4 AI Agents** | HR, Aptitude, Technical, DSA — each with custom prompts |
| 💬 **Chat Interface** | Real-time conversational interview UI |
| 🎯 **Live Scoring** | Every answer scored 1–10 with strengths & improvements |
| 📈 **Radar Chart** | Visual performance breakdown by round |
| 🏆 **Final Report** | Grade, verdict, analysis, and next steps |
| 🔒 **Session-based** | Each interview stored in PostgreSQL |

---

## 🚀 Quick Start

### Option A: Docker (Recommended)

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd ai-interview-simulator

# 2. Set up environment
cp .env.example .env
# Edit .env — add your GROQ_API_KEY

# 3. Run everything
docker compose up --build

# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option B: Manual Setup

#### Step 1 — PostgreSQL
```bash
# Using Docker just for DB:
docker run -d \
  --name ai_interview_db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=ai_interview_db \
  -p 5432:5432 \
  postgres:16-alpine

# Or install PostgreSQL locally and create the database:
# createdb ai_interview_db
```

#### Step 2 — Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp ../.env.example .env
# Edit .env — fill in GROQ_API_KEY and DATABASE_URL

# Initialize database tables
python init_db.py

# Start FastAPI server
uvicorn main:app --reload --port 8000
```

#### Step 3 — Frontend
```bash
cd frontend

# Install dependencies
pip install -r requirements.txt

# Start Streamlit
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🔑 API Keys

### Groq (Free, Required)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free)
3. Create API key
4. Add to `.env`: `GROQ_API_KEY=gsk_...`

The app uses **LLaMA 3.3 70B** via Groq's free tier — extremely fast inference.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/resume/upload` | Upload and parse resume |
| `GET` | `/api/resume/score/{token}` | Get resume score |
| `POST` | `/api/interview/start` | Start a round |
| `POST` | `/api/interview/answer` | Submit answer |
| `GET` | `/api/interview/history/{token}` | Get chat history |
| `GET` | `/api/evaluation/results/{token}` | Full results |
| `GET` | `/api/evaluation/score-prediction/{token}` | Score prediction |
| `GET` | `/api/sessions/{token}` | Session info |

Interactive API docs: **http://localhost:8000/docs**

---

## 🗄️ Database Schema

```
users
  └── interview_sessions
        ├── round_results
        │     └── question_answers
        └── chat_messages
```

---

## 🎮 Interview Flow

```
Upload Resume (PDF/DOCX)
        ↓
Resume Parsing + Scoring
        ↓
HR Round      (3 behavioral questions)
        ↓
Aptitude Round (3 logical/math questions)
        ↓
Technical Round (3 resume-based questions)
        ↓
DSA Round     (3 coding/algo questions)
        ↓
Final Report  (grade + radar chart + feedback)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit + Plotly |
| **Backend** | FastAPI + Uvicorn |
| **AI/LLM** | Groq API (LLaMA 3.3 70B) |
| **Resume Parsing** | pdfplumber + python-docx |
| **Database** | PostgreSQL + SQLAlchemy |
| **Containerization** | Docker + Docker Compose |

---

## 🔧 Configuration

Edit `.env` to customize:

```env
GROQ_API_KEY=gsk_your_key_here
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_interview_db
```

Edit `backend/services/interview_service.py`:
- `QUESTIONS_PER_ROUND = 3`  ← change number of questions per round
- `ROUNDS = ["HR", "APTITUDE", "TECHNICAL", "DSA"]` ← change round order

---

## 🚧 Roadmap

- [ ] Voice interview (Whisper STT + TTS)
- [ ] Code execution sandbox (Judge0 API)
- [ ] Adaptive difficulty (easier/harder based on performance)
- [ ] Resume vs Job Description matching score
- [ ] User accounts + historical performance dashboard
- [ ] Email report delivery

---

## 📝 License

MIT License — use freely for personal and commercial projects.
