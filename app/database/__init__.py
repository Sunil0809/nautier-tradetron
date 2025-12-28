"""Database connection and session management"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from app.utils import settings
import logging

logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session():
    """Context manager for database sessions"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_all_tables():
    """Create all tables"""
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")


def drop_all_tables():
    """Drop all tables (careful!)"""
    from app.models import Base
    Base.metadata.drop_all(bind=engine)
    logger.warning("All database tables dropped")
