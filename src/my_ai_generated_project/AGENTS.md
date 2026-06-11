# AGENTS.md — AI Agent Collaboration Guide

Guidelines for AI agents (Claude Code, Copilot, etc.) working in this repository.

## Project Context

This is a **Python FastAPI e-commerce marketplace API**. It is a greenfield project targeting B2C consumers. Auth is handled entirely by Firebase; the backend only verifies Firebase JWT tokens — it never issues its own tokens.

## Repository Layout

```
app/
├── main.py
├── core/           # Config, DB, Firebase init
├── models/         # SQLAlchemy models (one file per domain entity)
├── schemas/        # Pydantic v2 schemas (separate request/response models)
├── routers/        # FastAPI routers (thin — delegate to services)
├── services/       # Business logic (pure functions or classes, no FastAPI imports)
└── dependencies/   # Reusable FastAPI Depends() callables
docs/               # All project documentation
tests/
├── unit/           # Pure logic tests (no DB)
└── integration/    # Tests using a real in-memory SQLite DB
```

## Coding Conventions

- **Python 3.11+** — use `match`, `Self`, `ExceptionGroup` where appropriate.
- **Pydantic v2** — use `model_config`, `model_validator`, `field_validator`; never use v1 `@validator`.
- **SQLAlchemy 2.x async** — use `AsyncSession`, `select()`, never legacy `Query` API.
- **Routers are thin** — no business logic in route handlers. All logic lives in `services/`.
- **Schemas are separate** — never expose SQLAlchemy models directly. Always use Pydantic response schemas.
- **Dependency injection** — shared concerns (current user, DB session, pagination) go in `dependencies/`.

## Authentication Rules

- Firebase Admin SDK verifies ID tokens in `app/core/firebase.py`.
- The `get_current_user` dependency decodes the token and looks up or creates the user record.
- Never store or re-issue tokens. Never implement password auth — Firebase owns that.
- Role checks use `Depends(require_role("admin"))` pattern.

## Database Rules

- SQLite for local dev; the DATABASE_URL env var points to the right engine.
- All schema changes go through **Alembic migrations** — never use `Base.metadata.create_all()` in production.
- Use `CASCADE` deletes on child tables. Add DB-level `CHECK` constraints for enums.
- Never do N+1 queries — use `selectinload` or `joinedload` in service layer.

## Testing Rules

- Every new endpoint needs at least one integration test.
- Use `pytest-asyncio` with an in-memory SQLite fixture — no mocking the DB.
- Firebase token verification is mocked via `unittest.mock.patch` on `firebase_admin.auth.verify_id_token`.
- Run tests: `pytest tests/ -v`

## API Design Rules

- RESTful resource paths: `/api/v1/{resource}/{id}`.
- Pagination on all list endpoints: `?page=1&page_size=20`.
- Error responses follow RFC 9457 Problem Details format.
- Rate limiting headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`) on every response.

## What NOT to Do

- Do not add frontend code or HTML templates — this is a pure API project.
- Do not commit `.env` files or Firebase service account JSON.
- Do not bypass Firebase auth with a backdoor or hardcoded user.
- Do not use `print()` for logging — use the standard `logging` module or `structlog`.
- Do not use synchronous SQLAlchemy calls inside async route handlers.

## PR Checklist

- [ ] Alembic migration included for any schema changes
- [ ] Pydantic schemas updated (request + response)
- [ ] Integration test added
- [ ] `docs/` updated if the API surface changed
- [ ] No secrets committed
