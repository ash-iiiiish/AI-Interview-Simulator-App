from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import secrets

from database import get_db
from models import InterviewSession
from services.resume_service import (
    extract_text_from_pdf,
    extract_text_from_docx,
    parse_resume_with_llm,
    calculate_resume_score
)

router = APIRouter()


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and parse a resume PDF/DOCX file."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    filename_lower = file.filename.lower()
    if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".docx") or filename_lower.endswith(".doc")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    # Extract text
    try:
        if filename_lower.endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
        else:
            text = extract_text_from_docx(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not extract text from file: {str(e)}")

    if not text or len(text.strip()) < 50:
        raise HTTPException(status_code=422, detail="Could not extract meaningful text from the resume")

    # Parse with LLM
    try:
        resume_data = parse_resume_with_llm(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM parsing failed: {str(e)}")

    # Score the resume
    resume_score = calculate_resume_score(resume_data)
    resume_data["resume_score"] = resume_score

    # Create interview session
    session_token = secrets.token_hex(32)
    db_session = InterviewSession(
        session_token=session_token,
        resume_data=resume_data,
        current_round="HR",
        status="active"
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return {
        "session_token": session_token,
        "session_id": db_session.id,
        "resume_data": resume_data,
        "resume_score": resume_score,
        "message": "Resume parsed successfully! Ready to start interview."
    }


@router.get("/score/{session_token}")
async def get_resume_score(session_token: str, db: Session = Depends(get_db)):
    """Get the resume score for a session."""
    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    resume_data = session.resume_data or {}
    score = resume_data.get("resume_score") or calculate_resume_score(resume_data)

    return {"resume_score": score, "resume_data": resume_data}
