from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(200), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sessions = relationship("InterviewSession", back_populates="user")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_token = Column(String(64), unique=True, index=True)
    resume_data = Column(JSON)  # parsed resume JSON
    current_round = Column(String(20), default="HR")
    status = Column(String(20), default="active")  # active, completed
    overall_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="sessions")
    rounds = relationship("RoundResult", back_populates="session")
    messages = relationship("ChatMessage", back_populates="session")


class RoundResult(Base):
    __tablename__ = "round_results"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"))
    round_name = Column(String(20))  # HR, DSA, APTITUDE, TECHNICAL
    score = Column(Float, nullable=True)
    max_score = Column(Float, default=10.0)
    feedback = Column(Text, nullable=True)
    questions_asked = Column(Integer, default=0)
    completed = Column(Integer, default=0)  # 0 or 1

    session = relationship("InterviewSession", back_populates="rounds")
    answers = relationship("QuestionAnswer", back_populates="round_result")


class QuestionAnswer(Base):
    __tablename__ = "question_answers"

    id = Column(Integer, primary_key=True, index=True)
    round_result_id = Column(Integer, ForeignKey("round_results.id"))
    question = Column(Text)
    answer = Column(Text)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    round_result = relationship("RoundResult", back_populates="answers")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"))
    role = Column(String(10))  # user, assistant
    content = Column(Text)
    round_name = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("InterviewSession", back_populates="messages")
