# Auto memory, Postgram   (written by Claude, not you)
# This is an EXAMPLE of what ~/.claude/projects/<project>/memory/MEMORY.md accumulates.

## Build & run
- Backend uses SQLite when `DATABASE_URL` is unset (see app/db.py).
- Frontend dev server proxies `/api` to :8000 (vite.config.ts).

## Gotchas learned
- Pydantic v2: use `model_config = ConfigDict(from_attributes=True)`, not `orm_mode`.
- Run pytest from `backend/` so `app` imports resolve.
- The likes endpoint is idempotent, a second POST is a no-op, do not 500.

## Preferences observed
- User wants the failing test written before the endpoint (TDD).
