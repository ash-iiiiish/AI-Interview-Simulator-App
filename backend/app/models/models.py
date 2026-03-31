"""
SQLAlchemy ORM models — all database tables.
Uses SQLAlchemy 2.x mapped_column style + relationship typing.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column, Integer, String, Float, Text,
    DateTime, ForeignKey, JSON, func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String(64), unique=True, index=True, nullable=False)
    resume_data = Column(JSON, nullable=True)
    current_round = Column(String(20), default="HR")
    status = Column(String(20), default="active")          # active | completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    rounds = relationship("RoundResult", back_populates="session", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class RoundResult(Base):
    __tablename__ = "round_results"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    round_name = Column(String(20), nullable=False)        # HR | APTITUDE | TECHNICAL | DSA
    score = Column(Float, nullable=True)
    questions_asked = Column(Integer, default=0)
    completed = Column(Integer, default=0)                 # 0 = in progress, 1 = done

    session = relationship("InterviewSession", back_populates="rounds")
    answers = relationship("QuestionAnswer", back_populates="round_result", cascade="all, delete-orphan")


class QuestionAnswer(Base):
    __tablename__ = "question_answers"

    id = Column(Integer, primary_key=True, index=True)
    round_result_id = Column(Integer, ForeignKey("round_results.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    round_result = relationship("RoundResult", back_populates="answers")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    role = Column(String(10), nullable=False)              # user | assistant
    content = Column(Text, nullable=False)
    round_name = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("InterviewSession", back_populates="messages")
