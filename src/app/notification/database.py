from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from config.config import AppConfig
from typing import Generator


base = declarative_base()

engine = create_engine(
        AppConfig.DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in AppConfig.DATABASE_URL else {}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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