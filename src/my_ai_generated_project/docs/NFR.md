# Non-Functional Requirements (NFR)

**Project:** MarketPlace API
**Last Updated:** 2026-06-11

---

## 1. Performance

| Requirement | Target | Measurement Method |
|---|---|---|
| Read endpoint response time (p95) | < 200ms | Load test with Locust; monitored via Railway metrics |
| Write endpoint response time (p95) | < 400ms | Load test with Locust |
| Checkout endpoint response time (p95) | < 600ms | Load test (includes stock check + order creation) |
| Full-text product search (p95) | < 200ms | FTS5 on indexed columns |
| DB query time (individual query p99) | < 50ms | SQLAlchemy event listeners in dev; pg_stat_statements in prod |

### Performance Design Choices
- Async SQLAlchemy (`AsyncSession`) throughout — no blocking I/O in event loop
- Firebase token verification cached in-process for 5 minutes
- `average_rating` and `review_count` denormalized on `products` — no aggregate query on every product list
- Pagination enforced on all list endpoints (max `page_size=100`)
- Database indexes on all FK columns and common filter columns (see `DATABASE_SCHEMA.md`)

---

## 2. Scalability

| Requirement | Target |
|---|---|
| Concurrent users | 1,000 simultaneous authenticated users |
| Requests per second (steady state) | 500 RPS |
| Requests per second (burst) | 1,500 RPS for up to 60 seconds |
| Database connections | Connection pool: min=5, max=20 per process |

### Scalability Design Choices
- Stateless application layer — horizontal scaling by adding Railway instances
- No server-side session state; all state in DB or Firebase token
- SQLite → PostgreSQL migration path via Alembic; no code changes required
- Connection pooling via SQLAlchemy `async_sessionmaker` with pool size tuning

---

## 3. Availability

| Requirement | Target |
|---|---|
| Uptime SLA | 99.5% monthly (MVP); target 99.9% post-MVP |
| Planned maintenance window | Sundays 02:00–04:00 UTC |
| Recovery Time Objective (RTO) | < 15 minutes |
| Recovery Point Objective (RPO) | < 1 hour |

### Availability Design Choices
- Railway auto-restart on crash
- Health check endpoint `GET /health` polled every 30s; restart triggered on failure
- Database daily backups via Railway backup feature

---

## 4. Security

See [SECURITY.md](SECURITY.md) for full detail. NFR summary:

| Requirement | Target |
|---|---|
| All traffic encrypted in transit | TLS 1.2+ enforced |
| Authentication required for all state changes | Firebase JWT on every mutation |
| Rate limiting | 60 req/min unauthenticated; 120 req/min authenticated |
| No sensitive data in logs | PII masked, Authorization headers stripped |
| Dependency vulnerabilities | No high/critical CVEs in production dependencies |
| Audit log retention | 90 days minimum |

---

## 5. Maintainability

| Requirement | Target |
|---|---|
| Test coverage | ≥ 80% line coverage (measured by pytest-cov) |
| Type coverage | 100% of public functions and service methods type-annotated |
| Linting | Ruff with no errors; mypy strict mode |
| Code review | All PRs require at least one approval |
| Documentation | API spec (OpenAPI) kept in sync with code; updated in same PR as implementation |

---

## 6. Observability

| Requirement | Target |
|---|---|
| Structured logging | JSON logs to stdout; captured by Railway |
| Error tracking | Sentry SDK integrated; all 5xx errors captured with context |
| Request tracing | `X-Request-ID` header on every response |
| Health endpoint | `GET /health` returns `{"status": "ok", "db": "ok"}` |
| Metrics | Response time, request count, error rate exported (Railway built-in) |

---

## 7. Usability (API Consumer UX)

| Requirement | Target |
|---|---|
| API documentation | Swagger UI at `/docs`, ReDoc at `/redoc` |
| Consistent error format | RFC 9457 Problem Details on all 4xx/5xx responses |
| Pagination | Consistent `page`/`page_size` on all list endpoints |
| Versioning | `/api/v1/` prefix; breaking changes increment version |

---

## 8. Compliance

| Requirement | Approach |
|---|---|
| Data protection (GDPR baseline) | Users can delete their account + personal data via `DELETE /users/me` |
| No PII in logs | Logging middleware strips emails and tokens |
| Firebase data processing | Governed by Google's Firebase DPA |
