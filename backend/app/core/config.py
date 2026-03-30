"""
Central configuration — all environment variables are loaded here.
Every other module imports from this file instead of calling os.getenv() directly.
"""

import os
from dotenv import load_dotenv

# Load .env from the backend directory (or project root via Docker env_file)
load_dotenv()


class Settings:
    # ── Groq LLM ──────────────────────────────────────────────────────────────
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Model used for all LLM agents
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # ── Database ───────────────────────────────────────────────────────────────
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/ai_interview_db"
    )

    # ── App ────────────────────────────────────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")

    # ── Interview Config ───────────────────────────────────────────────────────
    ROUNDS: list = ["HR", "APTITUDE", "TECHNICAL", "DSA"]
    QUESTIONS_PER_ROUND: int = 3

    ROUND_CONFIG: dict = {
        "HR": {
            "label": "HR Round",
            "description": "Behavioral & cultural fit questions",
            "color": "#6366f1",
            "icon": "👤",
        },
        "APTITUDE": {
            "label": "Aptitude Round",
            "description": "Quantitative & logical reasoning",
            "color": "#f59e0b",
            "icon": "🧮",
        },
        "TECHNICAL": {
            "label": "Technical Round",
            "description": "Domain & resume-based questions",
            "color": "#10b981",
            "icon": "💻",
        },
        "DSA": {
            "label": "DSA Round",
            "description": "Data structures & algorithms",
            "color": "#ef4444",
            "icon": "🔢",
        },
    }


settings = Settings()
