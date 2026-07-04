"""Tests for the likes router, including the idempotency guarantee."""
from __future__ import annotations

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def _create_post(client: AsyncClient) -> dict:
    response = await client.post(
        "/api/posts",
        json={"author": "demo", "image_url": "https://example.com/a.jpg", "caption": ""},
    )
    assert response.status_code == 201
    return response.json()


async def test_like_post_first_time_returns_count_one(client: AsyncClient) -> None:
    post = await _create_post(client)

    response = await client.post(f"/api/posts/{post['id']}/likes", json={"user": "ada"})

    assert response.status_code == 200
    assert response.json()["likes"] == 1


async def test_like_post_twice_same_user_is_idempotent(client: AsyncClient) -> None:
    post = await _create_post(client)

    first = await client.post(f"/api/posts/{post['id']}/likes", json={"user": "ada"})
    second = await client.post(f"/api/posts/{post['id']}/likes", json={"user": "ada"})

    assert first.status_code == 200
    assert second.status_code == 200  # not a 500
    assert second.json()["likes"] == 1  # second POST is a no-op


async def test_unlike_post_after_like_returns_count_zero(client: AsyncClient) -> None:
    post = await _create_post(client)
    await client.post(f"/api/posts/{post['id']}/likes", json={"user": "ada"})

    response = await client.request(
        "DELETE", f"/api/posts/{post['id']}/likes", json={"user": "ada"}
    )

    assert response.status_code == 200
    assert response.json()["likes"] == 0


async def test_like_unknown_post_returns_404(client: AsyncClient) -> None:
    response = await client.post("/api/posts/missing/likes", json={"user": "ada"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"
