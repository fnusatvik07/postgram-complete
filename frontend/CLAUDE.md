# Frontend · Postgram UI
React + Vite + TypeScript. Read this before changing anything under `frontend/`.

## Stack & conventions
- Function components + hooks only. No class components.
- TypeScript strict; never use `any`.
- Tailwind for styling; no inline style objects.
- Data fetching via TanStack Query; the API client lives in `src/api/client.ts`.
- camelCase in TS; map snake_case API fields at the client boundary.

## Layout
- `src/components/`, reusable UI
- `src/pages/`     , route-level screens
- `src/api/`       , typed client + query hooks
