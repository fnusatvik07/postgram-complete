"""Application factory and router registration.

The REST API is served under the `/api` prefix. CORS is open to the Vite dev
server so the frontend can talk to it during development.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import comments, likes, posts
from .db import init_db

ALLOWED_ORIGINS = ["http://localhost:5173"]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Postgram API", version="0.1.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(posts.router, prefix="/api")
    app.include_router(comments.router, prefix="/api")
    app.include_router(likes.router, prefix="/api")

    return app


app = create_app()
