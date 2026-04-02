"""resume_service.py — Extract text from PDF/DOCX and parse with Groq LLM."""

import io
import json
import re

import pdfplumber
from docx import Document
from groq import Groq

from app.core.config import settings

groq_client = Groq(api_key=settings.GROQ_API_KEY)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract raw text from a PDF file."""
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract raw text from a DOCX file."""
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def parse_resume_with_llm(text: str) -> dict:
    """Use Groq LLM to parse raw resume text into structured JSON."""

    prompt = f"""Parse this resume text and return ONLY valid JSON — no markdown, no extra text.

Resume:
{text[:3000]}

Return exactly this JSON structure:
{{
  "name": "<full name>",
  "email": "<email or empty string>",
  "phone": "<phone or empty string>",
  "skills": ["<skill1>", "<skill2>"],
  "technical_skills": ["<tech_skill1>", "<tech_skill2>"],
  "experience": [
    {{"role": "<job title>", "company": "<company>", "duration": "<duration>"}}
  ],
  "education": [
    {{"degree": "<degree>", "institution": "<institution>", "year": "<year>"}}
  ],
  "projects": [
    {{"name": "<project name>", "description": "<brief description>", "technologies": ["<tech>"]}}
  ]
}}"""

    response = groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=800,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)

    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        # Fallback — return minimal structure
        return {
            "name": "Candidate",
            "email": "",
            "phone": "",
            "skills": [],
            "technical_skills": [],
            "experience": [],
            "education": [],
            "projects": [],
        }
