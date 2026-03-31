"""
Resume Service — PDF/DOCX text extraction, LLM-based parsing, and resume scoring.
"""

import io
import json
import re

import pdfplumber
from docx import Document

from app.agents.llm_agents import groq_client
from app.core.config import settings


# ── Text Extraction ────────────────────────────────────────────────────────────

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract raw text from PDF bytes using pdfplumber."""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text.strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract raw text from DOCX bytes."""
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join(para.text for para in doc.paragraphs).strip()


# ── LLM Resume Parsing ─────────────────────────────────────────────────────────

def parse_resume_with_llm(resume_text: str) -> dict:
    """Use the Groq LLM to extract structured data from raw resume text."""

    prompt = f"""Extract structured information from this resume text and return ONLY valid JSON (no markdown).

Resume Text:
{resume_text[:4000]}

Return this exact JSON structure (use empty arrays if a section is not found):
{{
  "name": "Full Name",
  "email": "email@example.com",
  "phone": "phone number",
  "skills": ["skill1", "skill2"],
  "technical_skills": ["Python", "SQL", "React"],
  "soft_skills": ["Leadership", "Communication"],
  "projects": [
    {{"name": "Project Name", "description": "what it does", "technologies": ["tech1"]}}
  ],
  "experience": [
    {{"company": "Company Name", "role": "Job Title", "duration": "Jan 2023 - Present", "description": "what you did"}}
  ],
  "education": [
    {{"degree": "B.Tech CSE", "institution": "College Name", "year": "2024", "cgpa": "8.5"}}
  ],
  "certifications": ["cert1", "cert2"],
  "summary": "Brief professional summary from the resume"
}}"""

    response = groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)

    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {
            "name": "Unknown",
            "email": "",
            "phone": "",
            "skills": [],
            "technical_skills": [],
            "soft_skills": [],
            "projects": [],
            "experience": [],
            "education": [],
            "certifications": [],
            "summary": resume_text[:500],
        }


# ── Resume Scoring ─────────────────────────────────────────────────────────────

def _get_grade(percentage: float) -> str:
    if percentage >= 85:
        return "A+"
    elif percentage >= 75:
        return "A"
    elif percentage >= 65:
        return "B+"
    elif percentage >= 55:
        return "B"
    elif percentage >= 45:
        return "C"
    return "D"


def calculate_resume_score(resume_data: dict) -> dict:
    """Score a resume across multiple dimensions and return a breakdown."""

    score = 0
    feedback = []

    # Skills — 20 pts
    total_skills = len(resume_data.get("skills") or []) + len(resume_data.get("technical_skills") or [])
    skill_score = min(20, total_skills * 2)
    score += skill_score
    if total_skills < 5:
        feedback.append("Add more technical skills to strengthen your profile.")
    else:
        feedback.append(f"Good skill coverage with {total_skills} skills listed.")

    # Projects — 25 pts
    projects = resume_data.get("projects") or []
    project_score = min(25, len(projects) * 8)
    score += project_score
    if len(projects) == 0:
        feedback.append("Add at least 2–3 projects with clear descriptions and tech stack.")
    elif len(projects) < 2:
        feedback.append("Consider adding more projects to showcase your abilities.")
    else:
        feedback.append(f"Great! {len(projects)} projects show practical experience.")

    # Experience — 25 pts
    experience = resume_data.get("experience") or []
    exp_score = min(25, len(experience) * 10)
    score += exp_score
    if len(experience) == 0:
        feedback.append("Add internships, part-time work, or freelance experience.")
    else:
        feedback.append(f"{len(experience)} work experience entries look good.")

    # Education — 15 pts
    education = resume_data.get("education") or []
    edu_score = 15 if len(education) > 0 else 0
    score += edu_score
    if len(education) == 0:
        feedback.append("Add your educational qualifications.")

    # Contact info — 10 pts
    contact_score = (5 if resume_data.get("email") else 0) + (5 if resume_data.get("phone") else 0)
    score += contact_score

    # Certifications — 5 pts
    certs = resume_data.get("certifications") or []
    cert_score = min(5, len(certs) * 2)
    score += cert_score
    if certs:
        feedback.append(f"{len(certs)} certification(s) add credibility.")
    else:
        feedback.append("Consider adding relevant certifications (AWS, Google, etc.).")

    return {
        "score": round(score, 1),
        "max_score": 100,
        "percentage": round((score / 100) * 100, 1),
        "grade": _get_grade(score),
        "breakdown": {
            "skills": skill_score,
            "projects": project_score,
            "experience": exp_score,
            "education": edu_score,
            "contact": contact_score,
            "certifications": cert_score,
        },
        "feedback": feedback,
    }
