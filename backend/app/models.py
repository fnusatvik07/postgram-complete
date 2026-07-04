"""SQLModel tables for Postgram.

Conventions (see CLAUDE.md): IDs are UUID strings, timestamps are UTC.
"""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlmodel import Field, SQLModel, UniqueConstraint


def _new_id() -> str:
    return str(uuid4())


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Post(SQLModel, table=True):
    id: str = Field(default_factory=_new_id, primary_key=True)
    image_url: str
    caption: str = ""
    author: str
    created_at: datetime = Field(default_factory=_utcnow)


class Comment(SQLModel, table=True):
    id: str = Field(default_factory=_new_id, primary_key=True)
    post_id: str = Field(foreign_key="post.id", index=True)
    author: str
    body: str
    created_at: datetime = Field(default_factory=_utcnow)


class Like(SQLModel, table=True):
    # A user can like a post at most once -> enables idempotent likes.
    __table_args__ = (UniqueConstraint("post_id", "user", name="uq_like_post_user"),)

    id: str = Field(default_factory=_new_id, primary_key=True)
    post_id: str = Field(foreign_key="post.id", index=True)
    user: str = Field(index=True)
    created_at: datetime = Field(default_factory=_utcnow)
