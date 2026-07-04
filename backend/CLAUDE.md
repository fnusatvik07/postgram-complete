# Backend · Postgram API
FastAPI service. Read this before changing anything under `backend/`.

## Stack & conventions
- Python 3.12, FastAPI, SQLModel, Pydantic v2.
- Endpoints are `async def` and use an `AsyncSession`.
- snake_case everywhere; type-hint every function.
- Response models live in `app/schemas.py`; never return ORM models directly.

## Layout
- `app/main.py`  , app factory + router registration
- `app/api/`     , one router file per resource (`posts.py`, `comments.py`, `likes.py`)
- `app/models.py`, SQLModel tables
- `app/schemas.py`,  request/response models
- `app/db.py`    , engine + session

## Testing
- pytest + httpx AsyncClient. One test file per router.
- Arrange-Act-Assert. Cover the happy path AND one failure per endpoint.
