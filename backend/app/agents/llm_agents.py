"""
llm_agents.py — All AI/LLM logic using the free Groq API.

Model used: llama-3.3-70b-versatile (free on Groq).
Get your free API key at https://console.groq.com/keys
"""

import json
import re

from groq import Groq

from app.core.config import settings

# Single Groq client — reused for all calls
groq_client = Groq(api_key=settings.GROQ_API_KEY)


# ── System Prompts ─────────────────────────────────────────────────────────────

def _build_system_prompt(round_name: str, resume_data: dict) -> str:
    """Build a round-specific system prompt personalised with the candidate's resume."""

    def _join(items: list, limit: int = 8) -> str:
        return ", ".join(str(i) for i in items[:limit]) if items else "Not specified"

    skills    = resume_data.get("technical_skills") or resume_data.get("skills") or []
    projects  = resume_data.get("projects") or []
    name      = resume_data.get("name", "Candidate")

    proj_names = _join([
        p.get("name", "") if isinstance(p, dict) else str(p)
        for p in projects
    ], 3)

    candidate_summary = f"""
Candidate: {name}
Skills: {_join(skills)}
Projects: {proj_names}
""".strip()

    prompts = {
        "HR": f"""You are a professional HR interviewer.
{candidate_summary}
- Ask ONE behavioral question at a time (STAR format friendly).
- Focus on teamwork, leadership, communication, and motivation.
- Be warm and professional.
- Do NOT evaluate in your response — just ask the next question naturally.""",

        "TECHNICAL": f"""You are a senior technical interviewer.
{candidate_summary}
- Ask ONE technical question at a time based on the candidate's skills/projects.
- Cover concepts from their listed technologies.
- Be concise and rigorous.
- Do NOT reveal correct answers during the interview.""",

        "DSA": f"""You are a DSA interviewer at a top tech company.
{candidate_summary}
- Ask ONE coding/algorithmic question at a time.
- Start easier, increase difficulty gradually.
- Cover arrays, strings, trees, graphs, dynamic programming.
- Ask about time/space complexity.""",
    }

    return prompts.get(round_name, prompts["HR"])


# ── Generate Next Question ─────────────────────────────────────────────────────

def generate_question(
    round_name: str,
    resume_data: dict,
    chat_history: list,
    question_number: int,
) -> str:
    """Generate the next interview question using Groq LLM (free)."""

    system_prompt = _build_system_prompt(round_name, resume_data)
    messages: list[dict] = [{"role": "system", "content": system_prompt}]

    if not chat_history:
        opener = {
            "HR":        f"Start the HR round. Greet the candidate briefly, then ask behavioral question #{question_number}.",
            "TECHNICAL": f"Start the Technical round. Briefly introduce it, then ask technical question #{question_number}.",
            "DSA":       f"Start the DSA round. Briefly introduce it, then ask DSA question #{question_number}.",
        }
        messages.append({"role": "user", "content": opener.get(round_name, f"Ask question {question_number}.")})
    else:
        for msg in chat_history[-8:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": f"The candidate answered. Now ask question #{question_number} of this round."})

    response = groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=400,
        timeout=60
    )
    return response.choices[0].message.content.strip()


# ── Evaluate Answer ────────────────────────────────────────────────────────────

def evaluate_answer(
    round_name: str,
    question: str,
    answer: str,
    resume_data: dict,
) -> dict:
    """Score a candidate's answer and return structured feedback."""

    if not answer or len(answer.strip()) < 5:
        return {
            "score": 0,
            "feedback": "No meaningful answer provided.",
            "strengths": [],
            "improvements": ["Provide a detailed answer", "Don't skip questions"],
        }

    skills = resume_data.get("technical_skills") or resume_data.get("skills") or []

    prompt = f"""Evaluate this interview answer. Return ONLY valid JSON — no markdown, no extra text.

Round: {round_name}
Question: {question}
Answer: {answer}
Candidate Skills: {", ".join(str(s) for s in skills[:6])}

Return exactly this JSON:
{{
  "score": <number 1-10>,
  "feedback": "<2-3 sentence constructive feedback>",
  "strengths": ["<strength1>", "<strength2>"],
  "improvements": ["<improvement1>", "<improvement2>"]
}}"""

    response = groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=400,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)

    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {
            "score": 5,
            "feedback": "Your answer was received. Keep practising for clarity.",
            "strengths": ["Attempted the question"],
            "improvements": ["Be more specific", "Use concrete examples"],
        }


# ── Final Report ───────────────────────────────────────────────────────────────

def generate_final_report(
    resume_data: dict,
    round_scores: dict,
) -> dict:
    """Generate a comprehensive end-of-interview performance report."""

    scores_text = "\n".join([f"- {r}: {s:.1f}/10" for r, s in round_scores.items()])
    overall = sum(round_scores.values()) / len(round_scores) if round_scores else 0

    prompt = f"""Generate a brief interview performance report. Return ONLY valid JSON.

Candidate: {resume_data.get('name', 'Candidate')}
Round Scores:
{scores_text}
Overall: {overall:.1f}/10

Return exactly this JSON (no markdown):
{{
  "overall_score": {overall:.1f},
  "grade": "<A/B/C/D>",
  "verdict": "<Recommended/Maybe/Not Recommended>",
  "summary": "<2-3 sentence summary>",
  "top_strengths": ["<s1>", "<s2>", "<s3>"],
  "improvements": ["<i1>", "<i2>", "<i3>"],
  "next_steps": ["<step1>", "<step2>"]
}}"""

    response = groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=600,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)

    try:
        return json.loads(raw.strip())
    except Exception:
        return {
            "overall_score": overall,
            "grade": "B",
            "verdict": "Recommended",
            "summary": f"Candidate scored {overall:.1f}/10 overall.",
            "top_strengths": ["Completed all rounds"],
            "improvements": ["Practice more"],
            "next_steps": ["Review fundamentals", "Practice on LeetCode"],
        }
