"""Likes router: like (idempotent), unlike, and count.

Idempotency: a second POST from the same user is a no-op and returns 200 with the
current count, it must never 500.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..models import Like, Post
from ..schemas import LikeCount, LikeCreate

router = APIRouter(tags=["likes"])


async def _count_likes(session: AsyncSession, post_id: str) -> int:
    total = await session.scalar(
        select(func.count()).select_from(Like).where(Like.post_id == post_id)
    )
    return total or 0


@router.get(
    "/posts/{post_id}/likes",
    response_model=LikeCount,
    summary="Get the like count for a post",
)
async def get_like_count(
    post_id: str,
    session: AsyncSession = Depends(get_session),
) -> LikeCount:
    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return LikeCount(post_id=post_id, likes=await _count_likes(session, post_id))


@router.post(
    "/posts/{post_id}/likes",
    response_model=LikeCount,
    summary="Like a post (idempotent)",
)
async def like_post(
    post_id: str,
    payload: LikeCreate,
    session: AsyncSession = Depends(get_session),
) -> LikeCount:
    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    existing = await session.scalar(
        select(Like).where(Like.post_id == post_id, Like.user == payload.user)
    )
    if existing is None:  # first like -> insert; repeat like -> no-op
        session.add(Like(post_id=post_id, user=payload.user))
        await session.commit()

    return LikeCount(post_id=post_id, likes=await _count_likes(session, post_id))


@router.delete(
    "/posts/{post_id}/likes",
    response_model=LikeCount,
    summary="Unlike a post",
)
async def unlike_post(
    post_id: str,
    payload: LikeCreate,
    session: AsyncSession = Depends(get_session),
) -> LikeCount:
    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    existing = await session.scalar(
        select(Like).where(Like.post_id == post_id, Like.user == payload.user)
    )
    if existing is not None:
        await session.delete(existing)
        await session.commit()

    return LikeCount(post_id=post_id, likes=await _count_likes(session, post_id))
