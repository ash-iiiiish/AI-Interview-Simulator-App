"""
Database engine and session factory.
SQLAlchemy 2.0 style — declarative_base imported from sqlalchemy.orm (not
sqlalchemy.ext.declarative which is deprecated in 2.x).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


# ── Declarative Base (SQLAlchemy 2.x style) ───────────────────────────────────
class Base(DeclarativeBase):
    pass


# ── Engine & Session ──────────────────────────────────────────────────────────
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # Detect stale connections
    pool_recycle=3600,        # Recycle connections every 1 hour
    echo=False,               # Set True for SQL debug logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency — yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
