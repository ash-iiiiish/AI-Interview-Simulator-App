"""resume.py — Upload and parse a resume, create an interview session."""

import secrets

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import InterviewSession
from app.services.resume_service import (
    extract_text_from_pdf,
    extract_text_from_docx,
    parse_resume_with_llm,
)

router = APIRouter()


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a PDF or DOCX resume, parse it, and create an interview session."""

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    fname = file.filename.lower()
    if not (fname.endswith(".pdf") or fname.endswith(".docx") or fname.endswith(".doc")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="File is empty.")

    try:
        text = extract_text_from_pdf(file_bytes) if fname.endswith(".pdf") else extract_text_from_docx(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not extract text: {e}")

    if not text or len(text.strip()) < 50:
        raise HTTPException(status_code=422, detail="Could not extract enough text from the resume.")

    try:
        resume_data = parse_resume_with_llm(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM parsing failed: {e}")

    token = secrets.token_hex(32)
    session = InterviewSession(
        session_token=token,
        resume_data=resume_data,
        current_round="HR",
        status="active",
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_token": token,
        "resume_data": resume_data,
        "message": "Resume parsed! Ready to start your interview.",
    }
