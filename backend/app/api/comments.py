"""Comments router: add a comment to a post and list a post's comments (paginated)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..models import Comment, Post
from ..schemas import CommentCreate, CommentRead

router = APIRouter(tags=["comments"])


@router.get(
    "/posts/{post_id}/comments",
    response_model=list[CommentRead],
    summary="List comments on a post (paginated)",
)
async def list_comments(
    post_id: str,
    session: AsyncSession = Depends(get_session),
    limit: int = Query(20, ge=1, le=100, description="Max items to return."),
    offset: int = Query(0, ge=0, description="Items to skip."),
) -> list[CommentRead]:
    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    result = await session.execute(
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all())


@router.post(
    "/posts/{post_id}/comments",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a comment to a post",
)
async def add_comment(
    post_id: str,
    payload: CommentCreate,
    session: AsyncSession = Depends(get_session),
) -> CommentRead:
    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    comment = Comment(post_id=post_id, author=payload.author, body=payload.body)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment
