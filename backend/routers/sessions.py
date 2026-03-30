from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import InterviewSession, RoundResult

router = APIRouter()


@router.get("/{session_token}")
async def get_session(session_token: str, db: Session = Depends(get_db)):
    """Get session details."""
    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    round_results = db.query(RoundResult).filter(
        RoundResult.session_id == session.id
    ).all()

    return {
        "session_token": session_token,
        "current_round": session.current_round,
        "status": session.status,
        "resume_data": session.resume_data,
        "rounds_completed": [rr.round_name for rr in round_results if rr.completed],
        "created_at": session.created_at.isoformat() if session.created_at else None
    }


@router.delete("/{session_token}")
async def delete_session(session_token: str, db: Session = Depends(get_db)):
    """Delete a session."""
    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()
    return {"message": "Session deleted"}
