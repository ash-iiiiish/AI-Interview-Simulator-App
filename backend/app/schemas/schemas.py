"""
Pydantic v2 schemas — request bodies and response shapes for all API endpoints.
"""

from typing import Any, Optional
from pydantic import BaseModel, field_validator


# ── Interview ──────────────────────────────────────────────────────────────────

class StartRoundRequest(BaseModel):
    session_token: str
    round_name: Optional[str] = None


class AnswerRequest(BaseModel):
    session_token: str
    answer: str
    question: str
    round_name: str


# ── Responses ──────────────────────────────────────────────────────────────────

class EvaluationResult(BaseModel):
    score: float
    feedback: str
    strengths: list[str]
    improvements: list[str]
    sample_answer_hint: Optional[str] = None


class RoundDetail(BaseModel):
    score: float
    config: dict[str, Any]
    questions: list[dict[str, Any]]
