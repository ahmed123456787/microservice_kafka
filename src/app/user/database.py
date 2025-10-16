from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from config.config import AppConfig

# Create database engine
engine = create_engine(
    AppConfig.DATABASE_URL,
    # Add connect_args only for SQLite
    connect_args={"check_same_thread": False} if "sqlite" in AppConfig.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a SQLAlchemy session
    Yields the session and ensures it's closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()