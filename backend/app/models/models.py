from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    resume_data = Column(JSON, nullable=True)
    resume_filename = Column(String, nullable=True)
    current_round = Column(String, default="HR")
    status = Column(String, default="active")

    overall_score = Column(Float, nullable=True)
    overall_feedback = Column(Text, nullable=True)

    rounds = relationship("RoundResult", back_populates="session", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class RoundResult(Base):
    __tablename__ = "round_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("interview_sessions.id"), nullable=False)
    round_type = Column(String, nullable=False)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    questions_asked = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("InterviewSession", back_populates="rounds")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("interview_sessions.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    round_type = Column(String, nullable=True)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("InterviewSession", back_populates="messages")
