# Product Requirements Document (PRD)

**Project:** MarketPlace API
**Status:** Greenfield / Pre-MVP
**Date:** 2026-06-11
**Owner:** akhshyganesh

---

## 1. Problem Statement

Individual consumers lack a unified, trustworthy platform to discover products from independent sellers, complete purchases securely, and leave verified reviews — all through a fast, API-first experience that can power any frontend or mobile client.

## 2. Goals

| Goal | Success Metric |
|---|---|
| Allow buyers to browse and purchase products | Checkout conversion rate ≥ 3% at launch |
| Enable sellers to list and manage products | Seller onboarding < 10 minutes end-to-end |
| Deliver fast search and discovery | Product search response < 200ms (p95) |
| Maintain platform trust | Review fraud rate < 1% (verified-purchase gate) |

## 3. Non-Goals (v1)

- No native mobile app (API-first; clients are external)
- No real-time chat between buyer and seller (v2)
- No multi-currency or international tax handling (v2)
- No physical inventory warehouse integration (v2)

## 4. Users & Roles

| Role | Description |
|---|---|
| **Buyer** | Registered consumer who browses, adds to cart, and purchases |
| **Seller** | Registered vendor who creates and manages product listings |
| **Admin** | Platform staff who moderate content, manage users, and resolve disputes |
| **Guest** | Unauthenticated user who can browse products but not purchase |

## 5. Core Features

### 5.1 User Auth & Profiles
- Firebase Authentication for all identity management (email/password, Google SSO)
- Profile creation on first Firebase token verification
- Profile fields: display name, avatar URL, shipping addresses, phone
- Role assignment: default `buyer`; sellers self-register; admins assigned by existing admin

### 5.2 Product & Category Management
- Sellers can create, update, and delete their own products
- Products have: name, description, price, stock quantity, images (URLs), category, tags
- Category hierarchy (parent → child)
- Soft-delete products (preserve order history)

### 5.3 Cart & Checkout
- Persistent cart tied to authenticated user
- Cart items: product, quantity, price snapshot at add time
- Checkout validates stock, calculates totals, and creates an Order
- Order statuses: `pending` → `confirmed` → `shipped` → `delivered` → `cancelled`

### 5.4 Search & Filters
- Full-text search on product name and description (SQLite FTS5)
- Filter by: category, price range, seller, rating, in-stock only
- Sort by: relevance, price asc/desc, newest, top-rated

### 5.5 Reviews & Ratings
- Only buyers with a `delivered` order for the product can submit a review
- Review fields: star rating (1–5), title, body, optional images
- Aggregate rating updated on each review submission
- Admins can flag and remove reviews

### 5.6 Notifications
- In-app notifications stored in DB (order status changes, review replies)
- Email notifications via SendGrid (order confirmation, shipping update)
- Notification preferences per user

### 5.7 Roles & Permissions
- Role-based access control (RBAC): `buyer`, `seller`, `admin`
- Sellers can only modify their own resources
- Admins have full platform access

## 6. Constraints

- SQLite for MVP; must be migration-safe to PostgreSQL
- Firebase is the sole auth provider — no custom password handling
- Deployment target: Railway (PaaS) — no Kubernetes for MVP
- Response time SLA: p95 < 200ms for all read endpoints

## 7. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| SQLite write contention at scale | Medium | Migrate to PostgreSQL before scaling beyond 100 concurrent writes |
| Firebase token latency | Low | Cache verified tokens in memory for 5 min |
| Review spam/fraud | Medium | Verified-purchase gate + admin moderation queue |
| PaaS cold-start latency | Low | Keep dyno/instance warm with health-check pings |
