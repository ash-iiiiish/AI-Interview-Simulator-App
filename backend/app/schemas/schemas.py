"""schemas.py — Pydantic v2 request/response schemas."""

from typing import Optional
from pydantic import BaseModel


class StartRoundRequest(BaseModel):
    session_token: str
    round_name: Optional[str] = None


class AnswerRequest(BaseModel):
    session_token: str
    answer: str
    question: str
    round_name: str
