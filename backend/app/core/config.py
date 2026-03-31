"""
Central configuration — all environment variables loaded via pydantic-settings.
Pydantic v2 + pydantic-settings replaces the old os.getenv() pattern and is
fully compatible with Python 3.12+.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Groq LLM ──────────────────────────────────────────────────────────────
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # ── Database ───────────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/ai_interview_db"

    # ── App ────────────────────────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-in-production"
    BACKEND_URL: str = "http://localhost:8000"

    # ── Interview Config ───────────────────────────────────────────────────────
    ROUNDS: list[str] = ["HR", "APTITUDE", "TECHNICAL", "DSA"]
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
