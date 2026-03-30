"""Interview router — start a round, submit answers, get next questions."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.models import ChatMessage, InterviewSession, QuestionAnswer, RoundResult
from app.agents.llm_agents import generate_question, evaluate_answer
from app.schemas.schemas import AnswerRequest, StartRoundRequest

router = APIRouter()

ROUNDS = settings.ROUNDS
QUESTIONS_PER_ROUND = settings.QUESTIONS_PER_ROUND
ROUND_CONFIG = settings.ROUND_CONFIG


@router.get("/rounds")
async def get_rounds():
    return {"rounds": ROUNDS, "config": ROUND_CONFIG, "questions_per_round": QUESTIONS_PER_ROUND}


@router.post("/start")
async def start_interview(request: StartRoundRequest, db: Session = Depends(get_db)):
    """Start or resume a round — returns the first question."""

    session = db.query(InterviewSession).filter(InterviewSession.session_token == request.session_token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session.status == "completed":
        raise HTTPException(status_code=400, detail="Interview already completed.")

    round_name = request.round_name or session.current_round

    round_result = db.query(RoundResult).filter(
        RoundResult.session_id == session.id,
        RoundResult.round_name == round_name,
    ).first()

    if not round_result:
        round_result = RoundResult(session_id=session.id, round_name=round_name, questions_asked=0)
        db.add(round_result)
        db.commit()
        db.refresh(round_result)

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session.id, ChatMessage.round_name == round_name)
        .order_by(ChatMessage.id)
        .all()
    )
    chat_history = [{"role": m.role, "content": m.content} for m in messages]

    question_number = round_result.questions_asked + 1
    question = generate_question(round_name, session.resume_data, chat_history, question_number)

    db.add(ChatMessage(session_id=session.id, role="assistant", content=question, round_name=round_name))
    round_result.questions_asked = question_number
    db.commit()

    return {
        "question": question,
        "round_name": round_name,
        "round_config": ROUND_CONFIG.get(round_name, {}),
        "question_number": question_number,
        "total_questions": QUESTIONS_PER_ROUND,
    }


@router.post("/answer")
async def submit_answer(request: AnswerRequest, db: Session = Depends(get_db)):
    """Submit a candidate answer — evaluates it and returns next question or round transition."""

    session = db.query(InterviewSession).filter(InterviewSession.session_token == request.session_token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    round_name = request.round_name

    db.add(ChatMessage(session_id=session.id, role="user", content=request.answer, round_name=round_name))

    evaluation = evaluate_answer(round_name, request.question, request.answer, session.resume_data)

    round_result = db.query(RoundResult).filter(
        RoundResult.session_id == session.id,
        RoundResult.round_name == round_name,
    ).first()

    if not round_result:
        round_result = RoundResult(session_id=session.id, round_name=round_name, questions_asked=1)
        db.add(round_result)
        db.commit()
        db.refresh(round_result)

    db.add(QuestionAnswer(
        round_result_id=round_result.id,
        question=request.question,
        answer=request.answer,
        score=evaluation.get("score", 5),
        feedback=evaluation.get("feedback", ""),
    ))

    answered_count = db.query(QuestionAnswer).filter(QuestionAnswer.round_result_id == round_result.id).count() + 1
    is_round_complete = answered_count >= QUESTIONS_PER_ROUND

    next_question = None
    next_round = None
    is_interview_complete = False

    if is_round_complete:
        all_qas = db.query(QuestionAnswer).filter(QuestionAnswer.round_result_id == round_result.id).all()
        scores = [q.score for q in all_qas if q.score is not None] + [evaluation.get("score", 5)]
        round_result.score = sum(scores) / len(scores) if scores else 5
        round_result.completed = 1

        current_idx = ROUNDS.index(round_name) if round_name in ROUNDS else -1
        if current_idx < len(ROUNDS) - 1:
            next_round = ROUNDS[current_idx + 1]
            session.current_round = next_round
        else:
            session.status = "completed"
            is_interview_complete = True
    else:
        messages = (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session.id, ChatMessage.round_name == round_name)
            .order_by(ChatMessage.id)
            .all()
        )
        chat_history = [{"role": m.role, "content": m.content} for m in messages]
        chat_history.append({"role": "user", "content": request.answer})

        question_number = round_result.questions_asked + 1
        next_question = generate_question(round_name, session.resume_data, chat_history, question_number)

        db.add(ChatMessage(session_id=session.id, role="assistant", content=next_question, round_name=round_name))
        round_result.questions_asked = question_number

    db.commit()

    return {
        "evaluation": evaluation,
        "next_question": next_question,
        "is_round_complete": is_round_complete,
        "next_round": next_round,
        "next_round_config": ROUND_CONFIG.get(next_round, {}) if next_round else None,
        "is_interview_complete": is_interview_complete,
        "answered_in_round": answered_count,
    }


@router.get("/history/{session_token}")
async def get_chat_history(session_token: str, round_name: Optional[str] = None, db: Session = Depends(get_db)):
    session = db.query(InterviewSession).filter(InterviewSession.session_token == session_token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    query = db.query(ChatMessage).filter(ChatMessage.session_id == session.id)
    if round_name:
        query = query.filter(ChatMessage.round_name == round_name)

    messages = query.order_by(ChatMessage.id).all()
    return {"messages": [{"role": m.role, "content": m.content, "round": m.round_name} for m in messages]}
