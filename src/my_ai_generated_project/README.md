# MarketPlace API

A B2C e-commerce marketplace REST API built with Python FastAPI. Supports multi-vendor product listings, shopping cart, checkout, orders, reviews, and role-based access control — all backed by Firebase Authentication and SQLite via SQLAlchemy.

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (Python 3.11+) |
| ORM | SQLAlchemy (async) |
| Database | SQLite (dev) → PostgreSQL (prod) |
| Auth | Firebase Authentication (JWT verification) |
| Deployment | PaaS — Railway / Render / Heroku |

## Quick Start

```bash
# 1. Clone and install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Fill in FIREBASE_PROJECT_ID, DATABASE_URL, etc.

# 3. Run database migrations
alembic upgrade head

# 4. Start the development server
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc`.

## Project Structure

```
app/
├── main.py              # FastAPI app factory
├── core/
│   ├── config.py        # Settings via pydantic-settings
│   ├── database.py      # SQLAlchemy engine & session
│   └── firebase.py      # Firebase Admin SDK init & token verification
├── models/              # SQLAlchemy ORM models
├── schemas/             # Pydantic request/response schemas
├── routers/             # Route handlers (users, products, orders, etc.)
├── services/            # Business logic layer
└── dependencies/        # FastAPI dependencies (auth, pagination, etc.)
docs/                    # Project documentation
tests/                   # Pytest test suite
```

## Core Modules

- **Users & Auth** — Firebase token verification, user profiles, role management (buyer, seller, admin)
- **Products & Categories** — Product CRUD, category hierarchy, image metadata, inventory tracking
- **Cart & Orders** — Shopping cart management, checkout flow, order lifecycle (pending → shipped → delivered)
- **Sellers** — Vendor onboarding, storefronts, seller dashboards
- **Reviews & Ratings** — Verified-purchase reviews, star ratings, moderation queue
- **Search & Notifications** — Full-text product search, filters, in-app and email notifications

## Documentation

| Doc | Description |
|---|---|
| [PRD](docs/PRD.md) | Product requirements and success metrics |
| [User Stories](docs/USER_STORIES.md) | Epics and user stories |
| [Architecture](docs/ARCHITECTURE.md) | System design and component diagram |
| [Database Schema](docs/DATABASE_SCHEMA.md) | Entity-relationship model |
| [API Spec](docs/API_SPEC.yaml) | OpenAPI 3.1 specification |
| [Security](docs/SECURITY.md) | Threat model and controls |
| [NFR](docs/NFR.md) | Non-functional requirements |
| [UI/UX](docs/UI_UX.md) | API consumer UX guidelines |
| [Decisions](docs/DECISIONS.md) | Architecture decision records |
| [Roadmap](docs/ROADMAP.md) | Milestones and delivery plan |

## Contributing

See [AGENTS.md](AGENTS.md) for AI agent collaboration guidelines and development workflow.
