"""Tests for the posts router: happy path plus one failure per endpoint."""
from __future__ import annotations

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def _create_post(client: AsyncClient, author: str = "demo") -> dict:
    response = await client.post(
        "/api/posts",
        json={
            "author": author,
            "image_url": "https://example.com/a.jpg",
            "caption": "hello",
        },
    )
    assert response.status_code == 201
    return response.json()


async def test_create_post_valid_payload_returns_201(client: AsyncClient) -> None:
    payload = {"author": "demo", "image_url": "https://example.com/a.jpg", "caption": "hi"}

    response = await client.post("/api/posts", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["author"] == "demo"
    assert body["like_count"] == 0
    assert body["comment_count"] == 0


async def test_create_post_missing_author_returns_422(client: AsyncClient) -> None:
    payload = {"image_url": "https://example.com/a.jpg"}

    response = await client.post("/api/posts", json=payload)

    assert response.status_code == 422


async def test_list_posts_after_create_returns_the_post(client: AsyncClient) -> None:
    created = await _create_post(client)

    response = await client.get("/api/posts")

    assert response.status_code == 200
    ids = [post["id"] for post in response.json()]
    assert created["id"] in ids


async def test_list_posts_limit_over_max_returns_422(client: AsyncClient) -> None:
    await _create_post(client)

    response = await client.get("/api/posts", params={"limit": 500})

    assert response.status_code == 422


async def test_get_post_existing_id_returns_200(client: AsyncClient) -> None:
    created = await _create_post(client)

    response = await client.get(f"/api/posts/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


async def test_get_post_unknown_id_returns_404(client: AsyncClient) -> None:
    response = await client.get("/api/posts/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


async def test_delete_post_existing_id_returns_detail(client: AsyncClient) -> None:
    created = await _create_post(client)

    response = await client.delete(f"/api/posts/{created['id']}")

    assert response.status_code == 200
    assert response.json()["detail"] == "Post deleted"


async def test_delete_post_unknown_id_returns_404(client: AsyncClient) -> None:
    response = await client.delete("/api/posts/nope")

    assert response.status_code == 404


async def test_add_comment_increments_comment_count(client: AsyncClient) -> None:
    created = await _create_post(client)

    add = await client.post(
        f"/api/posts/{created['id']}/comments",
        json={"author": "ada", "body": "nice shot"},
    )
    fetched = await client.get(f"/api/posts/{created['id']}")

    assert add.status_code == 201
    assert fetched.json()["comment_count"] == 1


async def test_add_comment_to_unknown_post_returns_404(client: AsyncClient) -> None:
    response = await client.post(
        "/api/posts/missing/comments",
        json={"author": "ada", "body": "hi"},
    )

    assert response.status_code == 404
