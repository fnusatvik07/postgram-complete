"""Posts router: create, read, list (paginated), delete.

Follows .claude/rules/api-design.md: every endpoint has a response_model + summary,
input is validated with Pydantic, errors use HTTPException, lists paginate.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..models import Comment, Like, Post
from ..schemas import DetailResponse, PostCreate, PostRead

router = APIRouter(prefix="/posts", tags=["posts"])


async def _to_read(session: AsyncSession, post: Post) -> PostRead:
    """Build a PostRead, annotating it with like and comment counts."""
    like_count = await session.scalar(
        select(func.count()).select_from(Like).where(Like.post_id == post.id)
    )
    comment_count = await session.scalar(
        select(func.count()).select_from(Comment).where(Comment.post_id == post.id)
    )
    return PostRead(
        id=post.id,
        image_url=post.image_url,
        caption=post.caption,
        author=post.author,
        created_at=post.created_at,
        like_count=like_count or 0,
        comment_count=comment_count or 0,
    )


@router.get("", response_model=list[PostRead], summary="List posts (paginated feed)")
async def list_posts(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(20, ge=1, le=100, description="Max items to return."),
    offset: int = Query(0, ge=0, description="Items to skip."),
) -> list[PostRead]:
    result = await session.execute(
        select(Post).order_by(Post.created_at.desc()).limit(limit).offset(offset)
    )
    posts = result.scalars().all()
    return [await _to_read(session, post) for post in posts]


@router.post(
    "",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a post",
)
async def create_post(
    payload: PostCreate,
    session: AsyncSession = Depends(get_session),
) -> PostRead:
    post = Post(**payload.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return await _to_read(session, post)


@router.get("/{post_id}", response_model=PostRead, summary="Get a post by id")
async def get_post(
    post_id: str,
    session: AsyncSession = Depends(get_session),
) -> PostRead:
    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return await _to_read(session, post)


@router.delete("/{post_id}", response_model=DetailResponse, summary="Delete a post")
async def delete_post(
    post_id: str,
    session: AsyncSession = Depends(get_session),
) -> DetailResponse:
    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    await session.delete(post)
    await session.commit()
    return DetailResponse(detail="Post deleted")
