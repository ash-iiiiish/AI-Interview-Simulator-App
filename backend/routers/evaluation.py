from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import InterviewSession, RoundResult, QuestionAnswer
from services.interview_service import generate_final_feedback, ROUND_CONFIG

router = APIRouter()


@router.get("/results/{session_token}")
async def get_evaluation_results(session_token: str, db: Session = Depends(get_db)):
    """Get full evaluation results for a completed interview."""
    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get all round results
    round_results = db.query(RoundResult).filter(
        RoundResult.session_id == session.id
    ).all()

    round_scores = {}
    round_details = {}

    for rr in round_results:
        qas = db.query(QuestionAnswer).filter(
            QuestionAnswer.round_result_id == rr.id
        ).all()

        scores = [qa.score for qa in qas if qa.score is not None]
        avg_score = sum(scores) / len(scores) if scores else 0

        round_scores[rr.round_name] = avg_score
        round_details[rr.round_name] = {
            "score": avg_score,
            "config": ROUND_CONFIG.get(rr.round_name, {}),
            "questions": [
                {
                    "question": qa.question,
                    "answer": qa.answer,
                    "score": qa.score,
                    "feedback": qa.feedback
                }
                for qa in qas
            ]
        }

    # Generate final feedback if completed
    final_feedback = None
    if session.status == "completed" and round_scores:
        final_feedback = generate_final_feedback(
            resume_data=session.resume_data or {},
            round_scores=round_scores,
            all_answers=[]
        )

    overall = sum(round_scores.values()) / len(round_scores) if round_scores else 0

    return {
        "session_token": session_token,
        "status": session.status,
        "overall_score": round(overall, 2),
        "round_scores": round_scores,
        "round_details": round_details,
        "final_feedback": final_feedback,
        "resume_data": session.resume_data
    }


@router.get("/score-prediction/{session_token}")
async def predict_score(session_token: str, db: Session = Depends(get_db)):
    """Predict final score based on current performance."""
    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    round_results = db.query(RoundResult).filter(
        RoundResult.session_id == session.id
    ).all()

    completed_scores = []
    for rr in round_results:
        if rr.score is not None:
            completed_scores.append(rr.score)

    if not completed_scores:
        return {"predicted_score": None, "message": "Not enough data yet"}

    current_avg = sum(completed_scores) / len(completed_scores)
    # Simple prediction: weighted average with slight regression to mean
    predicted = current_avg * 0.85 + 5.0 * 0.15

    return {
        "predicted_score": round(predicted, 2),
        "current_average": round(current_avg, 2),
        "rounds_completed": len(completed_scores),
        "confidence": f"{min(95, len(completed_scores) * 25)}%"
    }
