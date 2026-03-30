from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ResumeData(BaseModel):
    skills: List[str] = []
    projects: List[str] = []
    experience: List[str] = []
    education: str = ""
    name: Optional[str] = None
    email: Optional[str] = None
    summary: Optional[str] = None


class SessionCreate(BaseModel):
    pass


class SessionResponse(BaseModel):
    id: str
    current_round: str
    status: str
    resume_data: Optional[Dict[str, Any]] = None
    resume_filename: Optional[str] = None
    overall_score: Optional[float] = None
    overall_feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    session_id: str
    content: str


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    round_type: Optional[str] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AnswerSubmit(BaseModel):
    session_id: str
    question: str
    answer: str
    round_type: str


class EvaluationResult(BaseModel):
    score: float
    feedback: str
    suggestions: List[str]
    strengths: List[str]


class RoundSummary(BaseModel):
    round_type: str
    score: float
    feedback: str
    completed: bool


class FinalReport(BaseModel):
    session_id: str
    overall_score: float
    overall_feedback: str
    round_summaries: List[RoundSummary]
    top_strengths: List[str]
    improvement_areas: List[str]
    hiring_recommendation: str
