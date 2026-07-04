"""Pydantic v2 request/response models.

Never return ORM models directly, every endpoint uses a schema here as its
`response_model`. `from_attributes=True` lets us build these from SQLModel rows.
"""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---- Posts ----------------------------------------------------------------
class PostCreate(BaseModel):
    image_url: str = Field(min_length=1)
    caption: str = ""
    author: str = Field(min_length=1)


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    image_url: str
    caption: str
    author: str
    created_at: datetime
    like_count: int = 0
    comment_count: int = 0


# ---- Comments -------------------------------------------------------------
class CommentCreate(BaseModel):
    author: str = Field(min_length=1)
    body: str = Field(min_length=1)


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    post_id: str
    author: str
    body: str
    created_at: datetime


# ---- Likes ----------------------------------------------------------------
class LikeCreate(BaseModel):
    user: str = Field(min_length=1)


class LikeCount(BaseModel):
    post_id: str
    likes: int


# ---- Generic --------------------------------------------------------------
class DetailResponse(BaseModel):
    detail: str
