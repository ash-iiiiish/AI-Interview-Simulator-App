"""evaluation.py — Final results and report."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import InterviewSession, QuestionAnswer, RoundResult
from app.agents.llm_agents import generate_final_report

router = APIRouter()


@router.get("/results/{session_token}")
async def get_results(session_token: str, db: Session = Depends(get_db)):
    """Return full evaluation results for a completed interview."""

    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    round_results = db.query(RoundResult).filter(RoundResult.session_id == session.id).all()

    round_scores: dict = {}
    round_details: dict = {}

    for rr in round_results:
        qas = db.query(QuestionAnswer).filter(QuestionAnswer.round_result_id == rr.id).all()
        scores = [qa.score for qa in qas if qa.score is not None]
        avg = sum(scores) / len(scores) if scores else 0.0
        round_scores[rr.round_name] = avg
        round_details[rr.round_name] = {
            "score": avg,
            "questions": [
                {"question": qa.question, "answer": qa.answer, "score": qa.score, "feedback": qa.feedback}
                for qa in qas
            ],
        }

    final_report = None
    if session.status == "completed" and round_scores:
        final_report = generate_final_report(
            resume_data=session.resume_data or {},
            round_scores=round_scores,
        )

    overall = sum(round_scores.values()) / len(round_scores) if round_scores else 0.0

    return {
        "status": session.status,
        "overall_score": round(overall, 2),
        "round_scores": round_scores,
        "round_details": round_details,
        "final_report": final_report,
        "resume_data": session.resume_data,
    }
