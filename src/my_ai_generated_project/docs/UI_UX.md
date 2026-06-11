# UI/UX — API Consumer Experience Guidelines

**Project:** MarketPlace API
**Scope:** This is a pure REST API (no frontend). This document defines the UX contract for API consumers — web/mobile clients integrating with the API.

---

## 1. API Design Principles

### Consistency First
- All resource paths follow `/api/v1/{resource}/{id}` — no exceptions
- All list endpoints return the same envelope: `{ items: [...], total: n, page: n, page_size: n }`
- All timestamps are ISO 8601 UTC: `"2026-06-11T14:30:00Z"`
- All IDs are UUIDs (strings) — never expose database integer PKs to clients

### Predictable Errors
Every error response follows [RFC 9457 Problem Details](https://datatracker.ietf.org/doc/html/rfc9457):

```json
{
  "type": "https://api.marketplace.example.com/errors/insufficient-stock",
  "title": "Insufficient Stock",
  "status": 422,
  "detail": "Product 'Blue Sneakers' only has 2 units in stock. Requested: 5."
}
```

Common error types:

| HTTP Status | When |
|---|---|
| 400 Bad Request | Malformed JSON or missing required fields |
| 401 Unauthorized | Missing or invalid Firebase token |
| 403 Forbidden | Valid token but insufficient role or ownership |
| 404 Not Found | Resource does not exist |
| 409 Conflict | Duplicate resource (e.g. already reviewed this product) |
| 422 Unprocessable | Business rule violation (out of stock, empty cart) |
| 429 Too Many Requests | Rate limit exceeded |
| 500 Internal Server Error | Unexpected server error |

### Rate Limit Transparency
Every response includes rate limit headers so clients can self-throttle:

```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1718110800
```

When rate-limited (429):
```
Retry-After: 42
```

---

## 2. Authentication Flow for Clients

Clients obtain a Firebase ID token, then include it on every request:

```
Authorization: Bearer <firebase-id-token>
```

Token refresh: Firebase SDK handles token refresh automatically. Clients should retry a 401 response once after refreshing the token before treating it as a hard failure.

---

## 3. Pagination

All list endpoints support:

```
GET /api/v1/products?page=2&page_size=20
```

Response:

```json
{
  "items": [...],
  "total": 143,
  "page": 2,
  "page_size": 20
}
```

Clients should use `total` and `page_size` to determine if more pages exist: `has_next = page * page_size < total`.

---

## 4. Search & Filtering

Product search supports multiple simultaneous filters:

```
GET /api/v1/products?q=running+shoes&category_id=5&min_price=50&max_price=200&min_rating=4&in_stock=true&sort=price_asc&page=1&page_size=20
```

Clients should debounce search input by 300ms before sending the request.

---

## 5. Optimistic Updates Guidance

For cart operations, clients can apply optimistic UI updates:
- **Add to cart** → show item immediately; revert if API returns 422 (out of stock)
- **Remove from cart** → remove immediately; revert if API returns 404 or 500
- **Order status** → always re-fetch from server; do not derive from local state

---

## 6. Notification Polling

The API does not support WebSockets (v1). Clients should poll for notifications:

```
GET /api/v1/notifications?unread_only=true
```

Recommended polling interval: 30 seconds when user is active; pause when app is backgrounded.

---

## 7. Image Handling

Product images are stored as URLs (e.g. from a CDN or Firebase Storage). The API returns `images` as an array ordered by `position`. Clients should:
- Display `images[0]` as the primary thumbnail
- Handle missing images gracefully with a placeholder

---

## 8. Seller Dashboard Guidance

Sellers access their own products via:
```
GET /api/v1/products?seller_id=<my-uuid>
```

Sellers access incoming orders via:
```
GET /api/v1/orders?seller_id=<my-uuid>
```

(Order list endpoint supports `seller_id` filter for authenticated sellers.)

---

## 9. Request IDs

Every response includes `X-Request-ID`. Clients should log this and include it in support requests to enable server-side log correlation.

---

## 10. Versioning Policy

- Current version: `v1`
- Breaking changes (field removal, type change, endpoint removal) → new `v2` prefix
- Additive changes (new optional fields, new endpoints) → backwards-compatible, deployed to `v1`
- `v1` maintained for minimum 12 months after `v2` launch
