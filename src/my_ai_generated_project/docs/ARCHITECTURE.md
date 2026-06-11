# Architecture

**Project:** MarketPlace API
**Stack:** Python FastAPI · SQLAlchemy · SQLite → PostgreSQL · Firebase Auth · Railway PaaS

---

## 1. System Overview

```
┌────────────────────────────────────────────────────────────┐
│                        Clients                             │
│         (Mobile App / Web SPA / Third-party)               │
└───────────────────────┬────────────────────────────────────┘
                        │ HTTPS REST  (Bearer: Firebase ID Token)
┌───────────────────────▼────────────────────────────────────┐
│                   Railway PaaS                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              FastAPI Application                     │  │
│  │                                                      │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │  │
│  │  │  Routers │→ │ Services │→ │  Repositories    │   │  │
│  │  │(HTTP in) │  │(business │  │ (SQLAlchemy ORM) │   │  │
│  │  └────┬─────┘  │  logic)  │  └────────┬─────────┘   │  │
│  │       │        └──────────┘           │              │  │
│  │  ┌────▼─────────────────┐    ┌────────▼─────────┐   │  │
│  │  │   Dependencies       │    │   SQLite / PG DB │   │  │
│  │  │  (Auth, Pagination,  │    │   (SQLAlchemy    │   │  │
│  │  │   Rate Limit)        │    │    Async)        │   │  │
│  │  └──────────────────────┘    └──────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
                        │
          ┌─────────────▼──────────────┐
          │      Firebase Auth         │
          │  (Token verification only) │
          └────────────────────────────┘
```

## 2. Application Layers

### 2.1 Routers (Transport Layer)
- Located in `app/routers/`
- One module per resource: `users`, `products`, `categories`, `cart`, `orders`, `reviews`, `notifications`
- Responsibilities: parse HTTP request, call service, return HTTP response
- No business logic — 100% delegation to services

### 2.2 Services (Business Logic Layer)
- Located in `app/services/`
- Pure async functions or stateless classes
- No FastAPI imports — fully testable without HTTP
- Enforce business rules: stock validation, role checks, verified-purchase gate

### 2.3 Models (Data Layer)
- Located in `app/models/`
- SQLAlchemy 2.x `DeclarativeBase` mapped classes
- One file per domain entity
- Alembic manages all schema migrations

### 2.4 Schemas (Contract Layer)
- Located in `app/schemas/`
- Pydantic v2 models for request validation and response serialization
- Separate `CreateSchema`, `UpdateSchema`, `ResponseSchema` per entity
- No ORM objects ever leak through the API boundary

### 2.5 Dependencies (Cross-cutting Concerns)
- Located in `app/dependencies/`
- `get_db` — yields an `AsyncSession`
- `get_current_user` — verifies Firebase token, returns `User` ORM object
- `require_role(role)` — raises 403 if user lacks the role
- `get_pagination` — parses `page` / `page_size` query params

## 3. Authentication Flow

```
Client                 FastAPI               Firebase Admin SDK
  │                       │                         │
  │── POST /auth/login ──▶│                         │
  │  (Firebase ID token)  │── verify_id_token() ──▶│
  │                       │◀── decoded token ───────│
  │                       │── lookup/create User ──▶│DB
  │◀─── 200 + UserSchema ─│
```

The API **never** issues tokens. It only verifies Firebase-issued tokens on every request.

## 4. Request Lifecycle

1. HTTPS request hits Railway reverse proxy
2. FastAPI routes to the matching router
3. `get_current_user` dependency verifies Firebase token (5-min in-memory cache)
4. `require_role` dependency checks RBAC
5. Router delegates to service function
6. Service uses repository pattern to query/mutate DB via `AsyncSession`
7. Pydantic response schema serializes the result
8. Rate-limit middleware increments counter; adds headers to response

## 5. Data Flow: Checkout

```
POST /api/v1/orders/checkout
  → validate cart not empty
  → for each cart item: check stock >= quantity
  → create Order record (status=pending)
  → create OrderItem records (price snapshot)
  → decrement product stock
  → clear cart
  → emit order_confirmed notification (async task)
  → return OrderResponseSchema
```

## 6. Deployment Architecture (Railway)

```
railway.toml
├── Web service: uvicorn app.main:app --host 0.0.0.0 --port $PORT
├── Environment variables: DATABASE_URL, FIREBASE_PROJECT_ID, SECRET_KEY
└── Health check: GET /health → 200
```

- Single process per dyno for MVP
- SQLite volume-mounted for persistence (dev/staging)
- PostgreSQL add-on for production

## 7. Key Design Decisions

See [DECISIONS.md](DECISIONS.md) for full ADRs. Summary:
- Firebase Auth chosen to avoid building auth infrastructure from scratch
- SQLite for MVP to reduce ops burden; Alembic ensures zero-friction migration to PostgreSQL
- Repository pattern avoided (services call SQLAlchemy directly) to reduce abstraction layers for a small team
- No background task queue for MVP — notifications sent synchronously; move to Celery/Redis in v2
