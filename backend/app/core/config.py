from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/interview_simulator"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    GROQ_MODEL: str = "llama3-70b-8192"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
