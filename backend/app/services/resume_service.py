import pdfplumber
import re
from typing import Optional
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from app.core.config import settings
import json
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text.strip()


async def parse_resume_with_llm(resume_text: str) -> dict:
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL,
        temperature=0.1,
    )

    system_prompt = """You are an expert resume parser. Extract structured information from resumes.
Return ONLY valid JSON with these exact keys:
{
  "name": "candidate full name or null",
  "email": "email address or null",
  "skills": ["list", "of", "technical", "skills"],
  "projects": ["project 1 description", "project 2 description"],
  "experience": ["job 1 with company and duration", "job 2 with company"],
  "education": "highest education degree and institution",
  "summary": "2-3 sentence professional summary"
}
Return ONLY the JSON object, no markdown, no explanation."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Parse this resume:\n\n{resume_text[:4000]}")
    ]

    response = await llm.ainvoke(messages)
    
    try:
        raw = response.content.strip()
        # Strip markdown code blocks if present
        if raw.startswith("```"):
            raw = re.sub(r"```[a-z]*\n?", "", raw).strip().rstrip("```").strip()
        return json.loads(raw)
    except Exception:
        return {
            "name": None,
            "email": None,
            "skills": extract_skills_fallback(resume_text),
            "projects": [],
            "experience": [],
            "education": "",
            "summary": resume_text[:300]
        }


def extract_skills_fallback(text: str) -> list:
    common_skills = [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust",
        "React", "Angular", "Vue", "Node.js", "Django", "FastAPI", "Flask", "Spring",
        "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Docker", "Kubernetes",
        "AWS", "Azure", "GCP", "Git", "Linux", "Machine Learning", "Deep Learning",
        "TensorFlow", "PyTorch", "Pandas", "NumPy", "REST API", "GraphQL"
    ]
    found = []
    text_lower = text.lower()
    for skill in common_skills:
        if skill.lower() in text_lower:
            found.append(skill)
    return found
