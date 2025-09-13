"""Database configuration and session management."""

from typing import Optional
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()
engine: Optional[create_engine] = None
SessionLocal: Optional[sessionmaker] = None


def init_db(app: Flask) -> None:
    """Initialize database connection."""
    global engine, SessionLocal
    
    engine = create_engine(
        app.config["DATABASE_URL"],
        pool_pre_ping=True,
        pool_recycle=300,
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Get database session."""
    if SessionLocal is None:
        raise RuntimeError("Database not initialized")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session() -> Session:
    """Get database session (non-generator version)."""
    if SessionLocal is None:
        raise RuntimeError("Database not initialized")
    return SessionLocal()