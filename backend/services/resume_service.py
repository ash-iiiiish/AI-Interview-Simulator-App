import pdfplumber
import json
import re
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract raw text from PDF bytes."""
    import io
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text.strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract raw text from DOCX bytes."""
    from docx import Document
    import io
    doc = Document(io.BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()


def parse_resume_with_llm(resume_text: str) -> dict:
    """Use Groq LLM to extract structured data from resume text."""
    prompt = f"""Extract structured information from this resume text and return ONLY valid JSON.

Resume Text:
{resume_text[:4000]}

Return this exact JSON structure (fill in from resume, use empty arrays if not found):
{{
  "name": "Full Name",
  "email": "email@example.com",
  "phone": "phone number",
  "skills": ["skill1", "skill2", "skill3"],
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
}}

Return ONLY the JSON object, no markdown, no explanation."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=2000
    )

    raw = response.choices[0].message.content.strip()

    # Clean up potential markdown code blocks
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return basic structure
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
            "summary": resume_text[:500]
        }


def calculate_resume_score(resume_data: dict) -> dict:
    """Score a resume across multiple dimensions."""
    score = 0
    feedback = []
    max_score = 100

    # Skills (20 pts)
    total_skills = len(resume_data.get("skills", [])) + len(resume_data.get("technical_skills", []))
    skill_score = min(20, total_skills * 2)
    score += skill_score
    if total_skills < 5:
        feedback.append("Add more technical skills to strengthen your profile")
    else:
        feedback.append(f"Good skill coverage with {total_skills} skills listed")

    # Projects (25 pts)
    projects = resume_data.get("projects", [])
    project_score = min(25, len(projects) * 8)
    score += project_score
    if len(projects) == 0:
        feedback.append("Add at least 2-3 projects with clear descriptions and tech stack")
    elif len(projects) < 2:
        feedback.append("Consider adding more projects to showcase your abilities")
    else:
        feedback.append(f"Great! {len(projects)} projects show practical experience")

    # Experience (25 pts)
    experience = resume_data.get("experience", [])
    exp_score = min(25, len(experience) * 10)
    score += exp_score
    if len(experience) == 0:
        feedback.append("Add internships, part-time work, or freelance experience")
    else:
        feedback.append(f"{len(experience)} work experience entries look good")

    # Education (15 pts)
    education = resume_data.get("education", [])
    edu_score = 15 if len(education) > 0 else 0
    score += edu_score
    if len(education) == 0:
        feedback.append("Add your educational qualifications")

    # Contact Info (10 pts)
    contact_score = 0
    if resume_data.get("email"):
        contact_score += 5
    if resume_data.get("phone"):
        contact_score += 5
    score += contact_score

    # Certifications (5 pts)
    certs = resume_data.get("certifications", [])
    cert_score = min(5, len(certs) * 2)
    score += cert_score
    if len(certs) > 0:
        feedback.append(f"{len(certs)} certification(s) add credibility")
    else:
        feedback.append("Consider adding relevant certifications (AWS, Google, etc.)")

    return {
        "score": round(score, 1),
        "max_score": max_score,
        "percentage": round((score / max_score) * 100, 1),
        "grade": get_grade(score / max_score * 100),
        "breakdown": {
            "skills": skill_score,
            "projects": project_score,
            "experience": exp_score,
            "education": edu_score,
            "contact": contact_score,
            "certifications": cert_score
        },
        "feedback": feedback
    }


def get_grade(percentage: float) -> str:
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
    else:
        return "D"
