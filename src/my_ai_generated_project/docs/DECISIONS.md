# Architecture Decision Records (ADR)

**Project:** MarketPlace API

---

## ADR-001: Firebase Authentication over custom auth

**Date:** 2026-06-11
**Status:** Accepted

**Context:**
Building a marketplace requires user registration, login, password reset, and potentially social SSO. Building this from scratch requires significant security expertise and ongoing maintenance.

**Decision:**
Use Firebase Authentication as the identity provider. The API only verifies Firebase ID tokens — it never stores passwords or issues tokens.

**Consequences:**
- ✅ Zero auth infrastructure to build or maintain
- ✅ Google/Apple SSO, email/password, phone auth available out of the box
- ✅ Industry-standard token security (RS256 JWT, 1-hour expiry)
- ❌ Vendor lock-in to Firebase; migrating away requires re-issuing tokens
- ❌ Adds a network call per request (mitigated by in-process 5-min token cache)

---

## ADR-002: SQLite for MVP with Alembic migration path to PostgreSQL

**Date:** 2026-06-11
**Status:** Accepted

**Context:**
The project is greenfield. We need a database that has zero ops burden for MVP but can scale to production load.

**Decision:**
Use SQLite for local dev and MVP staging. All schema changes managed by Alembic. `DATABASE_URL` env var switches the engine. No SQLite-specific features used (no `PRAGMA` calls in code, no SQLite-specific types).

**Consequences:**
- ✅ No DB server to provision for local dev
- ✅ Zero-cost on Railway's free tier
- ✅ Alembic ensures schema migrations are DB-agnostic
- ❌ SQLite has limited write concurrency (WAL mode helps; max ~50 concurrent writes)
- ❌ No `ARRAY` or `JSONB` type support — tags stored as comma-separated strings for now
- **Migration trigger:** Switch to PostgreSQL when write concurrency > 50 req/s or team size > 3 engineers

---

## ADR-003: FastAPI with async SQLAlchemy over Django/Flask

**Date:** 2026-06-11
**Status:** Accepted

**Context:**
Python web framework selection for a greenfield API-first service.

**Decision:**
FastAPI with async SQLAlchemy 2.x.

**Consequences:**
- ✅ Native async support matches our SQLite/Postgres async driver
- ✅ Automatic OpenAPI spec generation from Pydantic models
- ✅ Pydantic v2 validation is fastest Python validation library
- ✅ Dependency injection is first-class — auth, DB session, pagination are clean
- ❌ Less opinionated than Django — team must establish conventions (we do this via AGENTS.md)
- ❌ Django ORM ecosystem (django-filter, DRF) not available

---

## ADR-004: No background task queue for MVP

**Date:** 2026-06-11
**Status:** Accepted (revisit at v2)

**Context:**
Notifications need to be sent on order events. Options: synchronous send, `BackgroundTasks` (FastAPI), or a proper queue (Celery + Redis).

**Decision:**
Use FastAPI's built-in `BackgroundTasks` for notification dispatch. No Redis or Celery for MVP.

**Consequences:**
- ✅ Zero infrastructure overhead
- ✅ Notifications sent within the same request lifecycle
- ❌ If the notification send fails, it fails silently (no retry)
- ❌ Long notification tasks could delay response (mitigated: tasks run after response is sent)
- **Revisit:** Add Celery + Redis when notification failure rate > 1% or send volume > 1,000/hour

---

## ADR-005: UUID primary keys over integer sequences

**Date:** 2026-06-11
**Status:** Accepted

**Context:**
Choosing between auto-increment integer PKs (simple, predictable) and UUIDs (opaque, non-guessable).

**Decision:**
UUID v4 for all primary user-facing entities (users, products, orders, reviews, notifications). Integer auto-increment for internal lookup tables (categories, product_images, cart_items).

**Consequences:**
- ✅ Non-guessable IDs prevent enumeration attacks (IDOR mitigation)
- ✅ IDs can be generated client-side or in application layer without DB round-trip
- ❌ Slightly larger storage and index size than integers
- ❌ UUID comparison slightly slower than integer comparison (negligible at our scale)

---

## ADR-006: Denormalize average_rating and review_count on products

**Date:** 2026-06-11
**Status:** Accepted

**Context:**
Product list endpoints need to show ratings. Computing `AVG(rating)` and `COUNT(*)` on every product list query would be expensive at scale.

**Decision:**
Store `average_rating` and `review_count` directly on the `products` table, updated atomically when a review is submitted or deleted.

**Consequences:**
- ✅ Product list queries are O(1) for ratings — no JOIN or aggregate needed
- ✅ Simplifies search/sort by rating
- ❌ Denormalized data can drift if update fails; mitigated by DB transaction wrapping review insert + product update
- ❌ Requires careful handling on review deletion

---

## ADR-007: Railway PaaS over self-hosted for MVP

**Date:** 2026-06-11
**Status:** Accepted

**Context:**
Deployment target for MVP. Options: self-hosted VPS, Kubernetes, or PaaS (Railway/Render/Heroku).

**Decision:**
Railway PaaS.

**Consequences:**
- ✅ Zero DevOps overhead — push to deploy
- ✅ Automatic HTTPS, environment variable management, log streaming
- ✅ SQLite volume mounts and PostgreSQL add-on available
- ❌ Less control over infrastructure compared to VPS/K8s
- ❌ Vendor pricing scales with usage; review at 100k req/day
