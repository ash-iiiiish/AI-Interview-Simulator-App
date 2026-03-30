"""
LLM Agents — ALL AI/LLM logic lives here.

The Groq client is instantiated ONCE using settings (which already called load_dotenv).
Every interview round and evaluation function is defined in this module.

Model structure:
  - groq_client  →  single Groq SDK instance (api_key from settings.GROQ_API_KEY)
  - get_system_prompt()  →  returns round-specific system prompt
  - generate_question()  →  asks the next interview question
  - evaluate_answer()    →  scores and gives feedback on a candidate answer
  - generate_final_feedback()  →  produces the end-of-interview report
"""

import json
import re
from groq import Groq

from app.core.config import settings

# ── Single Groq client instance ───────────────────────────────────────────────
# api_key is read from settings, which loaded it via load_dotenv in config.py
groq_client = Groq(api_key=settings.GROQ_API_KEY)


# ── System Prompts ─────────────────────────────────────────────────────────────

def get_system_prompt(round_name: str, resume_data: dict) -> str:
    """Build a round-specific system prompt personalised with the candidate's resume."""

    resume_summary = f"""
Candidate Profile:
- Name: {resume_data.get('name', 'Candidate')}
- Skills: {', '.join(resume_data.get('technical_skills', resume_data.get('skills', []))[:10])}
- Projects: {', '.join([
    p.get('name', '') if isinstance(p, dict) else str(p)
    for p in resume_data.get('projects', [])[:3]
])}
- Experience: {', '.join([
    (e.get('role', '') + ' at ' + e.get('company', '')) if isinstance(e, dict) else str(e)
    for e in resume_data.get('experience', [])[:2]
])}
- Education: {', '.join([
    e.get('degree', '') if isinstance(e, dict) else str(e)
    for e in resume_data.get('education', [])[:2]
])}
"""

    prompts = {
        "HR": f"""You are a professional HR interviewer conducting a behavioral interview.
{resume_summary}
Your role:
- Ask ONE behavioral question at a time (STAR format friendly)
- Focus on: teamwork, leadership, conflict resolution, motivation, goals
- Be warm, professional, and encouraging
- Keep questions concise and clear
- After the candidate answers, briefly acknowledge then ask the next question
- Do NOT evaluate in your response — just ask questions naturally""",

        "APTITUDE": f"""You are an aptitude test examiner conducting a quantitative reasoning assessment.
{resume_summary}
Your role:
- Ask ONE aptitude question at a time
- Cover: number series, percentages, ratios, profit/loss, time-speed-distance, logical puzzles
- Make questions clear with specific numbers
- After the candidate answers, say 'Got it.' or 'Noted.' then move to the next question
- Do NOT reveal if the answer is right or wrong during the round""",

        "TECHNICAL": f"""You are a senior technical interviewer conducting a domain knowledge interview.
{resume_summary}
Your role:
- Ask ONE technical question at a time based on the candidate's skills and projects
- Cover: concepts from their listed technologies, project architecture, problem-solving
- Ask follow-up questions about specific projects when relevant
- Be conversational but rigorous
- After an answer, say 'Interesting.' or 'I see.' then proceed""",

        "DSA": f"""You are a DSA interviewer at a top tech company.
{resume_summary}
Your role:
- Ask ONE coding/algorithmic question at a time
- Start with easier problems and increase difficulty
- Cover: arrays, strings, trees, graphs, dynamic programming, sorting
- Ask the candidate to explain their approach and time/space complexity
- Format questions clearly with examples""",
    }

    return prompts.get(round_name, prompts["HR"])


# ── Question Generation ────────────────────────────────────────────────────────

def generate_question(
    round_name: str,
    resume_data: dict,
    chat_history: list,
    question_number: int,
) -> str:
    """Generate the next interview question using the Groq LLM."""

    system_prompt = get_system_prompt(round_name, resume_data)
    messages = [{"role": "system", "content": system_prompt}]

    if not chat_history:
        intro_map = {
            "HR": f"Ask HR behavioral question #{question_number}. If it's the first, start with a brief friendly greeting and introduce the round.",
            "APTITUDE": f"Ask aptitude question #{question_number}. If first, briefly introduce the aptitude section.",
            "TECHNICAL": f"Ask technical question #{question_number} based on the candidate's resume. If first, briefly introduce the technical round.",
            "DSA": f"Ask DSA question #{question_number}. If first, briefly introduce the DSA coding round.",
        }
        messages.append({"role": "user", "content": intro_map.get(round_name, f"Ask question {question_number}.")})
    else:
        for msg in chat_history[-8:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": f"The candidate answered. Now ask question #{question_number} of this round."})

    response = groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()


# ── Answer Evaluation ──────────────────────────────────────────────────────────

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
            "feedback": "No meaningful answer provided. Please attempt the question.",
            "strengths": [],
            "improvements": ["Provide a detailed answer", "Don't skip questions"],
            "sample_answer_hint": "Aim for a complete, structured response.",
        }

    prompt = f"""You are evaluating an interview answer. Return ONLY valid JSON.

Round: {round_name}
Question: {question}
Candidate's Answer: {answer}

Candidate's background:
- Skills: {', '.join(resume_data.get('technical_skills', resume_data.get('skills', []))[:8])}
- Projects: {', '.join([p.get('name', '') if isinstance(p, dict) else str(p) for p in resume_data.get('projects', [])[:3]])}

Evaluate and return this exact JSON (no markdown, no extra text):
{{
  "score": <number 1-10>,
  "feedback": "<2-3 sentence constructive feedback>",
  "strengths": ["<strength1>", "<strength2>"],
  "improvements": ["<improvement1>", "<improvement2>"],
  "sample_answer_hint": "<brief hint on what a strong answer looks like>"
}}

Scoring guide:
- 9-10: Exceptional, comprehensive, impressive
- 7-8: Good, clear, mostly complete
- 5-6: Average, basic understanding shown
- 3-4: Weak, missing key points
- 1-2: Very poor or incorrect"""

    response = groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=600,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)

    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {
            "score": 5,
            "feedback": "Your answer was received. Keep practising to improve clarity.",
            "strengths": ["Attempted the question"],
            "improvements": ["Be more specific", "Provide concrete examples"],
            "sample_answer_hint": "Focus on structure and clarity.",
        }


# ── Final Report Generation ────────────────────────────────────────────────────

def generate_final_feedback(
    resume_data: dict,
    round_scores: dict,
    all_answers: list,
) -> dict:
    """Produce a comprehensive end-of-interview performance report."""

    scores_text = "\n".join([f"- {r}: {s:.1f}/10" for r, s in round_scores.items()])
    overall = sum(round_scores.values()) / len(round_scores) if round_scores else 0

    prompt = f"""Generate a comprehensive interview performance report. Return ONLY valid JSON.

Candidate: {resume_data.get('name', 'Candidate')}
Skills: {', '.join(resume_data.get('technical_skills', resume_data.get('skills', []))[:8])}

Round Scores:
{scores_text}
Overall Average: {overall:.1f}/10

Return this exact JSON (no markdown):
{{
  "overall_score": {overall:.1f},
  "overall_percentage": {(overall / 10) * 100:.0f},
  "grade": "<A+/A/B+/B/C/D>",
  "verdict": "<Strongly Recommended/Recommended/Maybe/Not Recommended>",
  "executive_summary": "<3-4 sentence overall performance summary>",
  "top_strengths": ["<strength1>", "<strength2>", "<strength3>"],
  "key_improvements": ["<improvement1>", "<improvement2>", "<improvement3>"],
  "round_analysis": {{
    "HR": "<1-2 sentence analysis>",
    "APTITUDE": "<1-2 sentence analysis>",
    "TECHNICAL": "<1-2 sentence analysis>",
    "DSA": "<1-2 sentence analysis>"
  }},
  "next_steps": ["<actionable step1>", "<actionable step2>", "<actionable step3>"],
  "resources": ["<learning resource1>", "<learning resource2>"]
}}"""

    response = groq_client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1000,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)

    try:
        return json.loads(raw.strip())
    except Exception:
        return {
            "overall_score": overall,
            "overall_percentage": (overall / 10) * 100,
            "grade": "B",
            "verdict": "Recommended",
            "executive_summary": f"Candidate scored {overall:.1f}/10 overall across all interview rounds.",
            "top_strengths": ["Completed all rounds", "Showed willingness to learn"],
            "key_improvements": ["Practice more DSA", "Improve communication"],
            "round_analysis": {r: f"Scored {s:.1f}/10" for r, s in round_scores.items()},
            "next_steps": ["Practice daily coding", "Review fundamentals"],
            "resources": ["LeetCode", "GeeksForGeeks"],
        }
