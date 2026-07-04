"""Demo data seeder.

Usage (from backend/):
    python -m app.seed --demo

Creates the tables (if needed) and inserts a handful of demo posts with a few
likes and comments so the feed is not empty during the workshop.
"""
from __future__ import annotations

import argparse
import asyncio

from sqlalchemy import select

from .db import async_session_maker, init_db
from .models import Comment, Like, Post

DEMO_POSTS = [
    {
        "author": "demo",
        "image_url": "https://picsum.photos/seed/postgram-1/600/600",
        "caption": "Morning light over the harbour ☕",
    },
    {
        "author": "ada",
        "image_url": "https://picsum.photos/seed/postgram-2/600/600",
        "caption": "Trail run before the standup.",
    },
    {
        "author": "grace",
        "image_url": "https://picsum.photos/seed/postgram-3/600/600",
        "caption": "New desk setup is finally done.",
    },
]


async def seed_demo() -> None:
    await init_db()

    async with async_session_maker() as session:
        existing = await session.scalar(select(Post))
        if existing is not None:
            print("Database already has posts; skipping seed.")
            return

        posts: list[Post] = []
        for data in DEMO_POSTS:
            post = Post(**data)
            session.add(post)
            posts.append(post)
        await session.flush()  # assign ids

        session.add(Comment(post_id=posts[0].id, author="ada", body="Gorgeous!"))
        session.add(Comment(post_id=posts[0].id, author="grace", body="Wish I was there."))
        session.add(Like(post_id=posts[0].id, user="ada"))
        session.add(Like(post_id=posts[0].id, user="grace"))
        session.add(Like(post_id=posts[1].id, user="demo"))

        await session.commit()

    print(f"Seeded {len(DEMO_POSTS)} demo posts.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the Postgram database.")
    parser.add_argument("--demo", action="store_true", help="Insert demo posts.")
    args = parser.parse_args()

    if not args.demo:
        parser.error("nothing to do: pass --demo to seed demo data")

    asyncio.run(seed_demo())


if __name__ == "__main__":
    main()
