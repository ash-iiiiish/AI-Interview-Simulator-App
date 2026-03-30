# ⬡ AI Interview Simulator

Multi-round AI-powered interview simulator with an avatar interviewer UI,
resume parsing, real-time evaluation, and a final performance report.

---

## Project Structure

```
ai-interview-simulator/
├── .env.example              ← copy to .env and fill in your keys
├── .gitignore
├── docker-compose.yml
│
├── backend/
│   ├── main.py               ← FastAPI entry point (run: uvicorn app.main:app)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── app/
│       ├── core/
│       │   ├── config.py     ← load_dotenv() lives here — single source of truth
│       │   └── database.py   ← SQLAlchemy engine + session
│       ├── models/
│       │   └── models.py     ← All ORM models (InterviewSession, RoundResult, etc.)
│       ├── schemas/
│       │   └── schemas.py    ← Pydantic request/response schemas
│       ├── agents/
│       │   └── llm_agents.py ← Groq client + all LLM agent functions (question gen, eval, report)
│       ├── services/
│       │   └── resume_service.py ← PDF/DOCX parsing + resume scoring
│       └── routers/
│           ├── resume.py
│           ├── interview.py
│           ├── evaluation.py
│           └── sessions.py
│
└── frontend/
    ├── app.py                ← Streamlit UI (avatar interviewer, rich CSS)
    ├── requirements.txt
    ├── Dockerfile
    └── .streamlit/
        └── config.toml
```

---

## Where is the LLM / Model Structure?

All LLM logic is in **`backend/app/agents/llm_agents.py`**:

- `groq_client` — single Groq SDK instance (reads `GROQ_API_KEY` from `settings`)
- `get_system_prompt()` — builds round-specific persona prompt
- `generate_question()` — generates the next interview question
- `evaluate_answer()` — scores the candidate's answer with structured JSON
- `generate_final_feedback()` — produces the end-of-interview report

The model (`llama-3.3-70b-versatile`) is configured in `app/core/config.py` via `GROQ_MODEL`.

---

## How `load_dotenv` Works

`load_dotenv()` is called **once**, in `backend/app/core/config.py`.
Every other module imports `settings` from there — no module calls `os.getenv()` directly.

```
.env
 └─► app/core/config.py  (load_dotenv + Settings class)
       ├─► app/core/database.py      (settings.DATABASE_URL)
       ├─► app/agents/llm_agents.py  (settings.GROQ_API_KEY, settings.GROQ_MODEL)
       └─► app/routers/*.py          (settings.ROUNDS, settings.ROUND_CONFIG)
```

Frontend reads `BACKEND_URL` via its own `load_dotenv()` call in `frontend/app.py`.

---

## Setup

### 1. Copy and fill `.env`

```bash
cp .env.example .env
```

Edit `.env`:
```
GROQ_API_KEY=gsk_...          # from https://console.groq.com
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_interview_db
BACKEND_URL=http://localhost:8000
SECRET_KEY=some-random-secret
```

### 2. Run with Docker (recommended)

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

### 3. Run locally (without Docker)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Make sure PostgreSQL is running and `DATABASE_URL` in `.env` points to it.

---

## Interview Rounds

| Round | Interviewer | Focus |
|---|---|---|
| **HR** | Sarah Chen | Behavioral, STAR method, cultural fit |
| **Aptitude** | Prof. Arjun | Math, logic, reasoning |
| **Technical** | Alex Rivera | Resume-based domain questions |
| **DSA** | Bot-9000 | Algorithms, data structures |

Each round has 3 questions. Answers are scored 1–10 with strengths and improvement tips.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/resume/upload` | Upload PDF/DOCX, parse resume, create session |
| GET | `/api/resume/score/{token}` | Get resume score |
| POST | `/api/interview/start` | Start/resume a round |
| POST | `/api/interview/answer` | Submit answer, get evaluation + next question |
| GET | `/api/interview/history/{token}` | Chat history |
| GET | `/api/evaluation/results/{token}` | Full results + final report |
| GET | `/api/sessions/{token}` | Session details |
| DELETE | `/api/sessions/{token}` | Delete session |
