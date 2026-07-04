# Postgram
A mini photo-sharing app. FastAPI backend + React frontend.

## Commands
- Backend (dev): `cd backend && uvicorn app.main:app --reload`
- Backend tests:  `cd backend && pytest`
- Frontend (dev): `cd frontend && npm run dev`
- Frontend build: `cd frontend && npm run build`

## Architecture
- `backend/` , FastAPI + SQLModel + SQLite. REST API under `/api`.
- `frontend/`, React + Vite + TypeScript + Tailwind.
- Contract: responses are JSON; errors use `{ "detail": "..." }`.

## Conventions (whole project)
- All timestamps are UTC, ISO-8601.
- IDs are UUID strings.
- Never commit secrets; put them in `.env` (gitignored).

## Git
- Conventional Commits (`feat:`, `fix:`, `test:`).
- Never push directly to `main`.

<!-- Team note: keep this file under 200 lines. Area-specific rules go in backend/ and frontend/ CLAUDE.md. -->
