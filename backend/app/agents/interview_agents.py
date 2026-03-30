from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from app.core.config import settings
from typing import List, Dict, Any
import json
import re


def get_llm(temperature: float = 0.7) -> ChatGroq:
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL,
        temperature=temperature,
    )


# ─── HR Agent ────────────────────────────────────────────────────────────────

async def hr_agent(resume_data: dict, history: List[Dict], question_num: int) -> str:
    llm = get_llm(temperature=0.8)
    
    system = f"""You are a professional HR interviewer conducting a behavioral interview.
Candidate Resume Summary:
- Name: {resume_data.get('name', 'Candidate')}
- Skills: {', '.join(resume_data.get('skills', [])[:8])}
- Experience: {', '.join(resume_data.get('experience', [])[:3])}
- Education: {resume_data.get('education', 'Not specified')}

Rules:
- Ask ONE behavioral/situational question at a time
- Use STAR method context (Situation, Task, Action, Result)
- Reference their actual experience when relevant
- Be warm but professional
- This is question {question_num} of 4 in the HR round
- Do NOT evaluate the answer here, just ask the next question naturally
- Keep questions concise and clear"""

    messages = [SystemMessage(content=system)]
    
    for msg in history[-6:]:
        if msg["role"] == "assistant":
            messages.append(HumanMessage(content=f"[Previous question you asked]: {msg['content']}"))
        else:
            messages.append(HumanMessage(content=f"[Candidate answered]: {msg['content']}"))

    messages.append(HumanMessage(content="Ask the next HR behavioral question now."))
    
    response = await llm.ainvoke(messages)
    return response.content


# ─── DSA Agent ───────────────────────────────────────────────────────────────

async def dsa_agent(resume_data: dict, history: List[Dict], question_num: int) -> str:
    llm = get_llm(temperature=0.6)
    
    skills = resume_data.get('skills', [])
    skill_str = ', '.join(skills[:5]) if skills else 'general programming'
    
    system = f"""You are a senior software engineer conducting a DSA/coding interview.
Candidate's tech stack: {skill_str}

Rules:
- Ask ONE DSA/algorithmic question at a time
- Vary difficulty: Q1=Easy, Q2=Medium, Q3=Hard, Q4=Medium
- This is question {question_num} of 4
- Include time/space complexity discussion prompts
- For coding questions, ask them to explain their approach first
- Topics: Arrays, Strings, Trees, Graphs, DP, Sorting, Searching, Recursion
- Keep the question clear with an example if needed"""

    messages = [SystemMessage(content=system)]
    
    for msg in history[-6:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=f"Candidate: {msg['content']}"))

    messages.append(HumanMessage(content="Ask the next DSA question."))
    
    response = await llm.ainvoke(messages)
    return response.content


# ─── Aptitude Agent ──────────────────────────────────────────────────────────

async def aptitude_agent(history: List[Dict], question_num: int) -> str:
    llm = get_llm(temperature=0.5)
    
    system = f"""You are conducting a quantitative aptitude and logical reasoning interview.

Rules:
- Ask ONE aptitude question at a time
- This is question {question_num} of 4
- Mix topics: Q1=Math/Percentage, Q2=Logical Reasoning, Q3=Data Interpretation, Q4=Verbal/Analytical
- Provide exact numbers and clear problem statements
- Include answer choices (A/B/C/D) for MCQ style
- Make questions appropriate for a software engineering role"""

    messages = [SystemMessage(content=system)]
    
    for msg in history[-4:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=f"Candidate: {msg['content']}"))

    messages.append(HumanMessage(content="Ask the next aptitude question."))
    
    response = await llm.ainvoke(messages)
    return response.content


# ─── Technical Agent ─────────────────────────────────────────────────────────

async def technical_agent(resume_data: dict, history: List[Dict], question_num: int) -> str:
    llm = get_llm(temperature=0.6)
    
    skills = resume_data.get('skills', [])
    projects = resume_data.get('projects', [])
    
    system = f"""You are a technical interviewer conducting a deep-dive technical interview.
Candidate's Skills: {', '.join(skills[:10])}
Candidate's Projects: {'; '.join(projects[:2])}

Rules:
- Ask ONE technical question at a time  
- This is question {question_num} of 4
- Questions should be resume-specific and in-depth
- Cover: system design concepts, frameworks they know, project decisions, architecture
- Ask about trade-offs and why they chose certain technologies
- Be precise and technical"""

    messages = [SystemMessage(content=system)]
    
    for msg in history[-6:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=f"Candidate: {msg['content']}"))

    messages.append(HumanMessage(content="Ask the next technical question based on their resume."))
    
    response = await llm.ainvoke(messages)
    return response.content


# ─── Evaluation Agent ────────────────────────────────────────────────────────

async def evaluate_answer(question: str, answer: str, round_type: str, resume_data: dict) -> dict:
    llm = get_llm(temperature=0.2)
    
    round_criteria = {
        "HR": "communication clarity, behavioral response quality, STAR method usage, cultural fit",
        "DSA": "algorithm correctness, time/space complexity analysis, code quality, problem-solving approach",
        "APTITUDE": "answer correctness, logical reasoning, calculation accuracy, approach explanation",
        "TECHNICAL": "technical accuracy, depth of knowledge, practical application, concept clarity"
    }
    
    criteria = round_criteria.get(round_type, "overall quality")
    
    system = """You are an expert interview evaluator. Evaluate answers and return ONLY valid JSON.
Return this exact JSON structure:
{
  "score": <number 1-10>,
  "feedback": "<2-3 sentence evaluation>",
  "strengths": ["strength 1", "strength 2"],
  "suggestions": ["improvement 1", "improvement 2"],
  "predicted_performance": "<Excellent/Good/Average/Below Average>"
}"""

    prompt = f"""Round: {round_type}
Evaluation Criteria: {criteria}
Candidate Skills: {', '.join(resume_data.get('skills', [])[:5])}

Question: {question}
Candidate Answer: {answer}

Evaluate this answer strictly but fairly."""

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=prompt)
    ]
    
    response = await llm.ainvoke(messages)
    
    try:
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = re.sub(r"```[a-z]*\n?", "", raw).strip().rstrip("```").strip()
        return json.loads(raw)
    except Exception:
        return {
            "score": 5.0,
            "feedback": "Your answer showed some understanding of the topic.",
            "strengths": ["Attempted the question"],
            "suggestions": ["Provide more detailed explanations", "Use specific examples"],
            "predicted_performance": "Average"
        }


# ─── Final Report Agent ──────────────────────────────────────────────────────

async def generate_final_report(session_data: dict) -> dict:
    llm = get_llm(temperature=0.3)
    
    system = """You are a senior hiring manager generating a final candidate assessment.
Return ONLY valid JSON with this structure:
{
  "overall_score": <number 1-10>,
  "overall_feedback": "<4-5 sentence comprehensive evaluation>",
  "top_strengths": ["strength 1", "strength 2", "strength 3"],
  "improvement_areas": ["area 1", "area 2", "area 3"],
  "hiring_recommendation": "<Strong Hire/Hire/Maybe/No Hire>",
  "recommended_role_level": "<Junior/Mid-level/Senior>",
  "key_insights": ["insight 1", "insight 2"]
}"""

    prompt = f"""Generate a final interview report for this candidate:

Resume: {json.dumps(session_data.get('resume_data', {}), indent=2)}

Round Scores:
{json.dumps(session_data.get('round_scores', {}), indent=2)}

Round Feedbacks:
{json.dumps(session_data.get('round_feedbacks', {}), indent=2)}

Provide a comprehensive, honest assessment."""

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=prompt)
    ]
    
    response = await llm.ainvoke(messages)
    
    try:
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = re.sub(r"```[a-z]*\n?", "", raw).strip().rstrip("```").strip()
        return json.loads(raw)
    except Exception:
        scores = session_data.get('round_scores', {})
        avg = sum(scores.values()) / len(scores) if scores else 5.0
        return {
            "overall_score": round(avg, 1),
            "overall_feedback": "The candidate completed all interview rounds.",
            "top_strengths": ["Completed all rounds", "Showed effort"],
            "improvement_areas": ["Technical depth", "Communication", "Problem solving"],
            "hiring_recommendation": "Maybe",
            "recommended_role_level": "Junior",
            "key_insights": ["Needs further evaluation"]
        }
