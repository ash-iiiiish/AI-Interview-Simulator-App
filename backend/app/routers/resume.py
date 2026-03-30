"""Resume router — upload and parse a candidate's resume."""

import secrets

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import InterviewSession
from app.services.resume_service import (
    calculate_resume_score,
    extract_text_from_docx,
    extract_text_from_pdf,
    parse_resume_with_llm,
)

router = APIRouter()


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a PDF or DOCX resume, parse it with the LLM, and create an interview session."""

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    fname = file.filename.lower()
    if not (fname.endswith(".pdf") or fname.endswith(".docx") or fname.endswith(".doc")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="File is empty.")

    # Extract text
    try:
        text = extract_text_from_pdf(file_bytes) if fname.endswith(".pdf") else extract_text_from_docx(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not extract text: {e}")

    if not text or len(text.strip()) < 50:
        raise HTTPException(status_code=422, detail="Could not extract meaningful text from the resume.")

    # Parse and score
    try:
        resume_data = parse_resume_with_llm(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM parsing failed: {e}")

    resume_data["resume_score"] = calculate_resume_score(resume_data)

    # Create session
    token = secrets.token_hex(32)
    session = InterviewSession(session_token=token, resume_data=resume_data, current_round="HR", status="active")
    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_token": token,
        "session_id": session.id,
        "resume_data": resume_data,
        "resume_score": resume_data["resume_score"],
        "message": "Resume parsed successfully! Ready to start interview.",
    }


@router.get("/score/{session_token}")
async def get_resume_score(session_token: str, db: Session = Depends(get_db)):
    """Return the resume score for an existing session."""

    session = db.query(InterviewSession).filter(InterviewSession.session_token == session_token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    resume_data = session.resume_data or {}
    score = resume_data.get("resume_score") or calculate_resume_score(resume_data)
    return {"resume_score": score, "resume_data": resume_data}
