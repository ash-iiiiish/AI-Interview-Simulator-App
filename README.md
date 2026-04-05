# 🎯 AI Interview Simulator

A clean, basic AI-powered interview simulator using **Groq (free LLM)** and **PostgreSQL**.

---

## 📁 Project Structure

```
ai-interview-simulator/
├── .env                          ← YOUR CONFIG FILE (edit this)
├── requirements.txt
├── docker-compose.yml
├── backend/
│   ├── main.py                   ← FastAPI entry point
│   ├── Dockerfile
│   └── app/
│       ├── core/
│       │   ├── config.py         ← Loads .env with load_dotenv()
│       │   └── database.py       ← PostgreSQL connection
│       ├── agents/
│       │   └── llm_agents.py     ← All Groq LLM logic
│       ├── models/models.py      ← Database tables (SQLAlchemy)
│       ├── routers/
│       │   ├── resume.py         ← /api/resume/upload
│       │   ├── interview.py      ← /api/interview/start + /answer
│       │   └── evaluation.py    ← /api/evaluation/results
│       ├── schemas/schemas.py    ← Pydantic request/response schemas
│       └── services/
│           └── resume_service.py ← PDF/DOCX text extraction
└── frontend/
    ├── app.py                    ← Streamlit UI
    ├── Dockerfile
    └── .streamlit/config.toml
```

---

## 🔑 Step 1 — Get Your FREE Groq API Key

1. Go to **https://console.groq.com/keys**
2. Sign up (no credit card required)
3. Click **Create API Key**
4. Copy the key

---

## ⚙️ Step 2 — Configure `.env`

Open the `.env` file in the project root and fill in:

```env
# Your free Groq API key (from console.groq.com/keys)
GROQ_API_KEY=gsk_your_key_here

# PostgreSQL connection string
# For Docker: keep as-is
# For local PostgreSQL: change user/password/dbname as needed
DATABASE_URL=postgresql://postgres:password@localhost:5432/interview_db

# Backend URL (Streamlit uses this to call FastAPI)
BACKEND_URL=http://localhost:8000
```

> ✅ **That's it!** Only 1 API key needed — Groq is completely free.

---

## 🐳 Option A — Run with Docker (Recommended)

```bash
# 1. Fill in .env (see above)

# 2. Build and start everything
docker-compose up --build

# 3. Open in browser
#    Frontend: http://localhost:8501
#    API docs: http://localhost:8000/docs
```

---

## 🐍 Option B — Run Locally (No Docker)

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running

### Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE interview_db;"

# 3. Fill in .env (set your GROQ_API_KEY and DATABASE_URL)

# 4. Start the backend (in one terminal)
cd backend
uvicorn main:app --reload --port 8000

# 5. Start the frontend (in another terminal)
streamlit run frontend/app.py
```

Open **http://localhost:8501** in your browser.

---

## 🎯 How the Interview Works

| Round | Questions | Focus |
|-------|-----------|-------|
| 👤 HR | 3 | Behavioral, teamwork, communication |
| 💻 Technical | 3 | Skills from your resume, project questions |
| 🔢 DSA | 3 | Data structures, algorithms, complexity |

Each answer is scored 1–10 with feedback. At the end, you get a full performance report.

---

## 🤖 LLM Model Used

- **Provider**: Groq (free tier)
- **Model**: `llama-3.3-70b-versatile`
- **Cost**: $0 — completely free
- **Rate limits**: Generous free limits; enough for full interviews

---

## 🗄️ Database Tables

| Table | Description |
|-------|-------------|
| `interview_sessions` | One per interview (links resume + rounds) |
| `round_results` | Score per round |
| `question_answers` | Each Q&A pair with score and feedback |
| `chat_messages` | Full chat history per round |

Tables are auto-created on first backend startup.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/resume/upload` | Upload PDF/DOCX resume |
| POST | `/api/interview/start` | Start a round, get first question |
| POST | `/api/interview/answer` | Submit answer, get next question |
| GET | `/api/evaluation/results/{token}` | Get full results + report |

Swagger UI: **http://localhost:8000/docs**



## 👨‍💻 Contributors
- [@ash-iiiiish](https://github.com/ash-iiiiish)

---

Tell me if there are some improvement needed....
