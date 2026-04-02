from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Find .env by searching from this file's location upward
_here = Path(__file__).resolve()
_env_path = _here.parent.parent.parent / ".env"  # backend/.env
if not _env_path.exists():
    _env_path = _here.parent.parent.parent.parent / ".env"  # root .env

load_dotenv(dotenv_path=_env_path, override=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_env_path),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/interview_db"
    BACKEND_URL: str = "http://localhost:8000"
    ROUNDS: list[str] = ["HR", "TECHNICAL", "DSA"]
    QUESTIONS_PER_ROUND: int = 3


settings = Settings()  # ← settings is created HERE

# Debug prints AFTER settings is created
print(f"Loading .env from: {_env_path}")
print(f"GROQ_API_KEY starts with: {settings.GROQ_API_KEY[:8]}...")