# Security

**Project:** MarketPlace API
**Last Updated:** 2026-06-11

---

## 1. Threat Model

| Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Stolen Firebase token reuse | Medium | High | Token expiry (1hr), Firebase revocation check |
| IDOR — accessing other users' resources | High | High | Owner check in every service before mutation |
| Mass product price tampering by seller | Low | Medium | Sellers can only update their own products |
| Review fraud (fake buyers) | Medium | Medium | Verified-purchase gate (delivered order required) |
| Brute-force / credential stuffing | Medium | High | Firebase handles; rate-limit our endpoints |
| SQL injection | Low | Critical | SQLAlchemy parameterized queries; no raw SQL |
| Sensitive data leakage in responses | Medium | High | Pydantic response schemas — never expose ORM objects |
| Insecure Direct Object Reference (IDOR) | High | High | UUID PKs + ownership checks |
| Denial of Service | Medium | Medium | Rate limiting middleware |
| Supply chain (dependency compromise) | Low | High | `pip-audit` in CI; pin dependencies in requirements.txt |

---

## 2. Authentication

- **Provider:** Firebase Authentication — we never handle passwords
- **Token type:** Firebase ID Token (RS256 JWT, 1-hour expiry)
- **Verification:** `firebase_admin.auth.verify_id_token()` on every authenticated request
- **Caching:** Decoded token cached in-memory for 5 minutes (keyed by token hash) to reduce Firebase API calls
- **Revocation:** Firebase handles token revocation; call `check_revoked=True` for high-privilege operations (role changes, account deletion)

## 3. Authorization (RBAC)

Roles: `buyer` < `seller` < `admin`

| Action | Buyer | Seller | Admin |
|---|---|---|---|
| Browse products | ✓ | ✓ | ✓ |
| Purchase products | ✓ | ✓ | ✓ |
| Create/edit own products | ✗ | ✓ | ✓ |
| Delete any product | ✗ | Own only | ✓ |
| Manage all users | ✗ | ✗ | ✓ |
| Remove reviews | ✗ | ✗ | ✓ |
| Promote user roles | ✗ | ✗ | ✓ |

Implementation: `require_role("seller")` dependency raises HTTP 403 if the authenticated user's role is insufficient.

**Ownership checks** — before any mutation, the service layer verifies `resource.owner_id == current_user.id` (unless the user is admin). This check happens in the service, not the router.

## 4. Input Validation

- All request bodies validated by Pydantic v2 before reaching the service layer
- Numeric fields have `gt=0` / `ge=0` constraints
- String fields have `max_length` limits to prevent oversized payloads
- UUIDs validated as proper UUID format — no sequential integer IDs exposed
- File URL fields validated as proper URIs

## 5. Rate Limiting

- Implemented via `slowapi` middleware (token bucket algorithm)
- Default: **60 requests/minute per IP** for unauthenticated endpoints
- Default: **120 requests/minute per user** for authenticated endpoints
- Stricter limits on mutation endpoints: **20 req/min** for `POST /orders/checkout`
- Headers returned: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- 429 response on breach with `Retry-After` header

## 6. Data Security

### Encryption in Transit
- All traffic over HTTPS (TLS 1.2+), enforced by Railway's reverse proxy
- HSTS header: `Strict-Transport-Security: max-age=31536000; includeSubDomains`

### Encryption at Rest
- SQLite database file encrypted via platform-level volume encryption (Railway)
- Firebase Auth data secured by Google's infrastructure

### Sensitive Field Handling
- Passwords: never stored — Firebase owns all credential data
- Firebase UID stored as an opaque string; never returned directly in user-facing responses where avoidable
- No PII logged — logging middleware strips `Authorization` headers and masks emails in log lines

## 7. Security Headers

All responses include:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'none'
Referrer-Policy: no-referrer
X-RateLimit-Limit: <n>
X-RateLimit-Remaining: <n>
```

## 8. Audit Logging

Every state-changing request is logged with:
- `user_id`, `role`
- HTTP method + path
- Resource ID affected
- Timestamp (UTC)
- IP address (hashed)
- Response status code

Logs are written to stdout in structured JSON (Railway captures and retains them).

## 9. Dependency Security

- `pip-audit` runs in CI on every PR — blocks merge on high/critical CVEs
- Dependencies pinned in `requirements.txt`
- Dependabot enabled for automated security PRs

## 10. Incident Response

1. Rotate Firebase service account key immediately
2. Set `DATABASE_URL` to read-only replica if DB compromise suspected
3. Force-revoke all Firebase tokens for affected users via Firebase Admin SDK
4. Notify affected users within 72 hours per GDPR Article 33
