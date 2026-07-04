# Postgram (complete): reference memory setup

The finished version of the workshop project. A small photo-sharing app (posts, likes,
comments) built with a **FastAPI backend** and a **React frontend**, wired up with a complete
Claude Code memory setup: `CLAUDE.md` files, path-scoped rules, settings, and an auto-memory example.

Use this repo two ways:
1. **As the answer key** for the live build.
2. **As a copy source**: paste these `CLAUDE.md` and rule files into the project you build in class,
   then push to GitHub.

The companion **`postgram-starter`** repo is the empty starting point you build from.

---

## The memory map: every file, and what it does

Each file below is a real, working example. The **Scope** column is the rule for deciding where
anything belongs.

| File | Scope | Who it is for | What it does |
|---|---|---|---|
| `CLAUDE.md` | project | the whole team | Project overview, build and test commands, and conventions true for the entire repo (UTC timestamps, UUID ids, error shape, git rules). |
| `backend/CLAUDE.md` | project (nested) | the API team | Backend-only rules. Loads when Claude reads a file under `backend/`: async endpoints, Pydantic v2, snake_case, schemas in `app/schemas.py`. |
| `frontend/CLAUDE.md` | project (nested) | the UI team | Frontend-only rules. Loads when Claude reads a file under `frontend/`: function components, no `any`, Tailwind, TanStack Query. |
| `.claude/rules/api-design.md` | project (path-scoped) | the API team | Applies to `backend/app/api/**`. Every endpoint declares `response_model` and `summary`, validates input, returns `{"detail": ...}` errors, and paginates lists. |
| `.claude/rules/testing.md` | project (path-scoped) | everyone | Applies to test files. Arrange-Act-Assert, `test_<unit>_<scenario>_<expected>` names, one test per new endpoint or component. |
| `.claude/rules/react.md` | project (path-scoped) | the UI team | Applies to `frontend/src/**/*.tsx`. One component per file, typed props, TanStack Query for server state, loading and error states required. |
| `.claude/settings.json` | project | the whole team | Committed permission allow-list (test and build commands) and `autoMemoryEnabled`. |
| `.claude/settings.local.json.example` | local | just you | Template for machine-local settings, with a `claudeMdExcludes` example. Copy to `settings.local.json` (gitignored). |
| `CLAUDE.local.md.example` | local | just you | Template for personal, uncommitted project notes (your port, seed command, review preference). Copy to `CLAUDE.local.md` (gitignored). |
| `docs/user-CLAUDE.md.example` | user | just you, all projects | Example of a `~/.claude/CLAUDE.md`. It lives in your home folder, not the repo, so it is kept here only as a reference to copy. |
| `MEMORY.example.md` | auto memory | Claude writes it | Example of what `~/.claude/projects/<project>/memory/MEMORY.md` accumulates. You never write this by hand; it is here so you can see what it looks like. |

**The decision rule.** Ask "who is this true for?"
- True for the repo, use project scope (`CLAUDE.md`, `.claude/rules/`)
- True for you on every project, use user scope (`~/.claude/CLAUDE.md`, `~/.claude/rules/`)
- True for your machine only, use local scope (`CLAUDE.local.md`, `.claude/settings.local.json`)
- Something Claude figured out, let auto memory keep it

---

## Copy these into your project during class

The three groups you paste into the project you build live:

```bash
# 1. the shared project files (committed)
CLAUDE.md
backend/CLAUDE.md
frontend/CLAUDE.md
.claude/settings.json
.claude/rules/api-design.md
.claude/rules/testing.md
.claude/rules/react.md

# 2. the personal templates (each person copies, fills in, then it stays gitignored)
cp CLAUDE.local.md.example              CLAUDE.local.md
cp .claude/settings.local.json.example  .claude/settings.local.json

# 3. the user file goes in your home folder, not the repo
cp docs/user-CLAUDE.md.example  ~/.claude/CLAUDE.md
```

`.gitignore` already excludes `CLAUDE.local.md`, `settings.local.json`, `.env`, and the SQLite db.

---

## Run the app

**Backend** (FastAPI, SQLModel, SQLite):

```bash
cd backend
pip install -r requirements.txt
python -m app.seed --demo       # optional: a few demo posts
uvicorn app.main:app --reload   # http://localhost:8000/docs
pytest                          # run the tests
```

**Frontend** (React, Vite, TypeScript, Tailwind):

```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173, proxies /api to :8000
```

---

## Layout

```
postgram-complete/
├── CLAUDE.md                       project instructions (shared)
├── CLAUDE.local.md.example         local template (copy to CLAUDE.local.md)
├── MEMORY.example.md               what auto memory accumulates
├── .claude/
│   ├── settings.json               permissions + autoMemoryEnabled
│   ├── settings.local.json.example local settings template
│   └── rules/                      api-design.md, testing.md, react.md
├── docs/
│   └── user-CLAUDE.md.example       example ~/.claude/CLAUDE.md (user scope)
├── backend/                        FastAPI app + tests, with backend/CLAUDE.md
└── frontend/                       React app, with frontend/CLAUDE.md
```

Source of the concepts: https://code.claude.com/docs/en/memory
