"""Database connection and session management using SQLModel."""

from collections.abc import Generator
from functools import lru_cache
import logging

from sqlmodel import Session, SQLModel, create_engine, text
from sqlalchemy import Engine

from config import settings

logger = logging.getLogger(__name__)


@lru_cache
def get_engine() -> Engine:
    """Get or create the database engine (lazy, cached).

    The engine is created on first access and cached for subsequent calls.
    This allows the application to import without requiring a database connection.
    """
    logger.info(f"Creating database engine for: {settings.database_url[:50]}...")

    try:
        engine = create_engine(
            settings.database_url,
            echo=settings.is_development,  # Log SQL in development
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,  # Recycle connections after 5 minutes
            connect_args={
                "connect_timeout": 10,
                "application_name": "evolution-todo-backend",
            },
        )

        # Test connection on creation
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")

        return engine
    except Exception as e:
        logger.error(f"❌ Failed to create database engine: {e}", exc_info=True)
        raise


def create_db_and_tables() -> None:
    """Create all database tables from SQLModel metadata.

    Note: In production, use Alembic migrations instead.
    """
    SQLModel.metadata.create_all(get_engine())


def get_session() -> Generator[Session, None, None]:
    """Dependency that provides a database session.

    Usage:
        @router.get("/items")
        def get_items(session: Session = Depends(get_session)):
            return session.exec(select(Item)).all()
    """
    with Session(get_engine()) as session:
        yield session
