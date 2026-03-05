"""
Database session configuration.

Creates:
- SQLAlchemy engine
- SessionLocal
- Base declarative class
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


# ---------------------------------------------------
# Database Engine
# ---------------------------------------------------

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.ECHO_QUERIES,
)


# ---------------------------------------------------
# Session Factory
# ---------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ---------------------------------------------------
# Base Class for Models
# ---------------------------------------------------

Base = declarative_base()


# ---------------------------------------------------
# Dependency (for FastAPI)
# ---------------------------------------------------

def get_db():
    """
    FastAPI dependency to provide DB session.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()