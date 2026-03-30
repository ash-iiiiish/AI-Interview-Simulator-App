from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ROUNDS = ["HR", "APTITUDE", "TECHNICAL", "DSA"]
QUESTIONS_PER_ROUND = 3

ROUND_CONFIG = {
    "HR": {
        "label": "HR Round",
        "description": "Behavioral & cultural fit questions",
        "color": "#6366f1",
        "icon": "👤"
    },
    "APTITUDE": {
        "label": "Aptitude Round",
        "description": "Quantitative & logical reasoning",
        "color": "#f59e0b",
        "icon": "🧮"
    },
    "TECHNICAL": {
        "label": "Technical Round",
        "description": "Domain & resume-based questions",
        "color": "#10b981",
        "icon": "💻"
    },
    "DSA": {
        "label": "DSA Round",
        "description": "Data structures & algorithms",
        "color": "#ef4444",
        "icon": "🔢"
    }
}


def get_system_prompt(round_name: str, resume_data: dict) -> str:
    resume_summary = f"""
Candidate Profile:
- Name: {resume_data.get('name', 'Candidate')}
- Skills: {', '.join(resume_data.get('technical_skills', resume_data.get('skills', []))[:10])}
- Projects: {', '.join([p.get('name', '') if isinstance(p, dict) else str(p) for p in resume_data.get('projects', [])[:3]])}
- Experience: {', '.join([e.get('role', '') + ' at ' + e.get('company', '') if isinstance(e, dict) else str(e) for e in resume_data.get('experience', [])[:2]])}
- Education: {', '.join([e.get('degree', '') if isinstance(e, dict) else str(e) for e in resume_data.get('education', [])[:2]])}
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
- After the candidate answers, say 'Got it.' or 'Noted.' then move to next question
- Do NOT reveal if answer is right or wrong during the round""",

        "TECHNICAL": f"""You are a senior technical interviewer conducting a domain knowledge interview.
{resume_summary}
Your role:
- Ask ONE technical question at a time based on the candidate's skills and projects
- Cover: concepts from their listed technologies, project architecture, problem-solving
- Ask follow-up questions based on their specific projects
- Be conversational but rigorous
- After an answer, say 'Interesting.' or 'I see.' then proceed""",

        "DSA": f"""You are a DSA interviewer at a top tech company.
{resume_summary}
Your role:
- Ask ONE coding/algorithmic question at a time
- Start with easier problems, increase difficulty
- Cover: arrays, strings, trees, graphs, dynamic programming, sorting
- Ask the candidate to explain their approach and complexity
- Be encouraging but technically rigorous
- Format questions clearly with examples"""
    }
    return prompts.get(round_name, prompts["HR"])


def generate_question(
    round_name: str,
    resume_data: dict,
    chat_history: list,
    question_number: int
) -> str:
    """Generate next interview question using Groq."""

    system_prompt = get_system_prompt(round_name, resume_data)

    messages = [{"role": "system", "content": system_prompt}]

    if not chat_history:
        # First question of the round
        intro_prompts = {
            "HR": f"Ask the {question_number}{'st' if question_number == 1 else 'nd' if question_number == 2 else 'rd' if question_number == 3 else 'th'} HR behavioral question. If it's the first question, start with a brief friendly greeting and introduce the round.",
            "APTITUDE": f"Ask aptitude question #{question_number}. If first, briefly introduce the aptitude section.",
            "TECHNICAL": f"Ask technical question #{question_number} based on the candidate's resume. If first, briefly introduce the technical round.",
            "DSA": f"Ask DSA question #{question_number}. If first, briefly introduce the DSA coding round."
        }
        messages.append({"role": "user", "content": intro_prompts.get(round_name, f"Ask question {question_number}")})
    else:
        # Continue with history
        for msg in chat_history[-8:]:  # last 8 messages for context
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": f"The candidate answered. Now ask question #{question_number} of this round."})

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()


def evaluate_answer(
    round_name: str,
    question: str,
    answer: str,
    resume_data: dict
) -> dict:
    """Evaluate a candidate's answer and return score + feedback."""

    if not answer or len(answer.strip()) < 5:
        return {
            "score": 0,
            "feedback": "No meaningful answer provided. Please attempt the question.",
            "strengths": [],
            "improvements": ["Provide a detailed answer", "Don't skip questions"]
        }

    prompt = f"""You are evaluating an interview answer. Return ONLY valid JSON.

Round: {round_name}
Question: {question}
Candidate's Answer: {answer}

Candidate's background:
- Skills: {', '.join(resume_data.get('technical_skills', resume_data.get('skills', []))[:8])}
- Projects: {', '.join([p.get('name', '') if isinstance(p, dict) else str(p) for p in resume_data.get('projects', [])[:3]])}

Evaluate and return this JSON:
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
- 1-2: Very poor or incorrect

Return ONLY the JSON object."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=600
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)

    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {
            "score": 5,
            "feedback": "Your answer was received. Keep practicing to improve clarity.",
            "strengths": ["Attempted the question"],
            "improvements": ["Be more specific", "Provide concrete examples"],
            "sample_answer_hint": "Focus on structure and clarity"
        }


def generate_final_feedback(
    resume_data: dict,
    round_scores: dict,
    all_answers: list
) -> dict:
    """Generate comprehensive final feedback and overall assessment."""

    scores_text = "\n".join([f"- {r}: {s:.1f}/10" for r, s in round_scores.items()])
    overall = sum(round_scores.values()) / len(round_scores) if round_scores else 0

    prompt = f"""Generate a comprehensive interview performance report. Return ONLY valid JSON.

Candidate: {resume_data.get('name', 'Candidate')}
Skills: {', '.join(resume_data.get('technical_skills', resume_data.get('skills', []))[:8])}

Round Scores:
{scores_text}
Overall Average: {overall:.1f}/10

Return this JSON:
{{
  "overall_score": {overall:.1f},
  "overall_percentage": {(overall/10)*100:.0f},
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
}}

Return ONLY the JSON object."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1000
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)

    try:
        return json.loads(raw.strip())
    except:
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
            "resources": ["LeetCode", "GeeksForGeeks"]
        }
