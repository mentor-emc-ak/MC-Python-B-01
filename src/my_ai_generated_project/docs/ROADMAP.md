# Roadmap

**Project:** MarketPlace API
**Current Stage:** Greenfield — Pre-MVP
**Goal:** Launch MVP to first users

---

## Milestone 0: Foundation (Weeks 1–2)

**Goal:** Runnable FastAPI app with CI/CD and auth wired up.

- [ ] Scaffold FastAPI project structure (`app/`, `tests/`, `docs/`)
- [ ] Configure SQLAlchemy async engine + Alembic
- [ ] Integrate Firebase Admin SDK — `verify_id_token` dependency
- [ ] Implement `users` table + `GET /users/me` + `PATCH /users/me`
- [ ] Set up `pytest` with async fixtures and in-memory SQLite
- [ ] Deploy to Railway with `GET /health` passing
- [ ] CI pipeline: lint (Ruff), type check (mypy), tests, `pip-audit`

**Done when:** A Firebase-authenticated user can fetch and update their profile in the deployed environment.

---

## Milestone 1: Products & Categories (Weeks 3–4)

**Goal:** Sellers can list products; buyers and guests can browse and search.

- [ ] `categories` table + `GET /categories`
- [ ] `products` + `product_images` tables
- [ ] `POST /products`, `GET /products/{id}`, `PATCH /products/{id}`, `DELETE /products/{id}`
- [ ] `GET /products` — pagination, filters (category, price, in-stock), sort
- [ ] SQLite FTS5 full-text search on name + description
- [ ] Seller role upgrade endpoint `POST /users/me/seller`
- [ ] RBAC: seller-only product creation + ownership check on update/delete

**Done when:** A seller can create a product and a guest can search and find it.

---

## Milestone 2: Cart & Checkout (Week 5)

**Goal:** Buyers can purchase products end-to-end.

- [ ] `cart_items` table + cart CRUD endpoints
- [ ] `POST /orders/checkout` — stock validation, order creation, stock decrement, cart clear
- [ ] `GET /orders` + `GET /orders/{id}`
- [ ] `POST /orders/{id}/cancel`
- [ ] `order_items` records with price snapshots
- [ ] In-app notification created on order_confirmed

**Done when:** A buyer can add items to cart, checkout, and see their order with status `confirmed`.

---

## Milestone 3: Reviews & Notifications (Week 6)

**Goal:** Verified buyers can review products; all users receive notifications.

- [ ] `reviews` table + `POST /products/{id}/reviews` (verified-purchase gate)
- [ ] `GET /products/{id}/reviews`
- [ ] `average_rating` + `review_count` updated atomically on review submit/delete
- [ ] Admin review flagging + removal
- [ ] `notifications` table + `GET /notifications` + `POST /notifications/{id}/read`
- [ ] Order status notification on `confirmed`, `shipped`, `delivered`

**Done when:** A buyer with a delivered order can submit a review and see notifications for their order status changes.

---

## Milestone 4: Hardening & Launch (Week 7–8)

**Goal:** Production-ready for first real users.

- [ ] Rate limiting via `slowapi` on all endpoints
- [ ] Security headers middleware
- [ ] Audit logging middleware (structured JSON)
- [ ] Sentry error tracking integrated
- [ ] Load test with Locust: verify p95 < 200ms at 500 RPS
- [ ] Switch Railway deployment to PostgreSQL add-on
- [ ] `DELETE /users/me` — GDPR account deletion
- [ ] Final security review (see `SECURITY.md`)
- [ ] Test coverage ≥ 80%

**Done when:** Load test passes, all security controls in place, deployed on PostgreSQL.

---

## v2 Backlog (Post-MVP)

| Feature | Notes |
|---|---|
| Seller analytics dashboard | Revenue, order volume, top products |
| Real-time notifications | WebSocket or SSE channel |
| Background task queue | Celery + Redis; replace `BackgroundTasks` |
| Payment integration | Stripe checkout; order status → `paid` |
| Product image upload | Firebase Storage integration |
| Multi-currency | Stripe handles currency; add `currency` field to products |
| Buyer–seller messaging | Chat threads per order |
| Admin moderation dashboard | Flagged reviews, seller applications queue |
| Mobile push notifications | Firebase Cloud Messaging (FCM) |
| Elasticsearch | Replace FTS5 when search volume demands it |
