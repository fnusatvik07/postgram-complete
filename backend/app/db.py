"""Database engine and session management.

Uses SQLite via aiosqlite by default; override with the ``DATABASE_URL``
environment variable. Sessions are `AsyncSession` per the backend conventions.
"""
from __future__ import annotations

import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

# SQLite when DATABASE_URL is unset. The file lives next to the app as postgram.db.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./postgram.db")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Create all tables. Called once on application startup."""
    # Import models so they are registered on SQLModel.metadata before create_all.
    from . import models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding an `AsyncSession`."""
    async with async_session_maker() as session:
        yield session
