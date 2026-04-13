"""
Database connection and session management
Handles async SQLAlchemy setup for SQLite
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager
import logging

from config.settings import Config

logger = logging.getLogger(__name__)

# Base class for all ORM models
Base = declarative_base()

# Create async engine (allows concurrent database operations)
engine = create_async_engine(
    Config.db_url,
    echo=False,  # Set to True to see SQL queries (debugging)
    future=True,
    pool_pre_ping=True,  # Verify connection before using it
)

# Create session factory for async operations
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True,
)


async def get_session():
    """
    Dependency injection for database session
    Usage: async with get_session() as session: ...
    """
    async with async_session_maker() as session:
        yield session


@asynccontextmanager
async def get_db():
    """
    Context manager for database operations
    Automatically handles commit/rollback/close

    Usage:
        async with get_db() as session:
            result = await session.execute(...)
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database tables
    Creates all tables defined in models
    """
    try:
        logger.info("Initializing database...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def close_db():
    """
    Close database connection
    Call this when shutting down the application
    """
    try:
        await engine.dispose()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error closing database: {e}")
        raise
