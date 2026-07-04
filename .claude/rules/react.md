---
paths:
  - "frontend/src/**/*.tsx"
---
# React component rules
- One component per file; PascalCase filename.
- Props typed with an explicit interface; never `any`.
- Server state via TanStack Query; local UI state via `useState`.
- Every data fetch renders a loading state and an error state.
