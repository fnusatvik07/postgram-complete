---
paths:
  - "backend/app/api/**/*.py"
---
# API design rules
- Every endpoint declares a `response_model` and a `summary`.
- Validate input with Pydantic; never trust raw query params.
- Errors use `HTTPException` with `{ "detail": "..." }`.
- List endpoints paginate: `limit` default 20, max 100.
