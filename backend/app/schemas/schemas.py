"""
Pydantic schemas — request bodies and response shapes for all API endpoints.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


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
    strengths: List[str]
    improvements: List[str]
    sample_answer_hint: Optional[str] = None


class RoundDetail(BaseModel):
    score: float
    config: Dict[str, Any]
    questions: List[Dict[str, Any]]
