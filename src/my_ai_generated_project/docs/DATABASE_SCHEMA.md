# Database Schema

**Project:** MarketPlace API
**ORM:** SQLAlchemy 2.x async
**Engine:** SQLite (dev) → PostgreSQL (prod)
**Migrations:** Alembic

---

## Entity Relationship Diagram

```
users ──────────────────────────────────────────────────────────────┐
  │ (seller_id)                                                      │
  │                                                                  │
  ├──< products >──< product_images                                  │
  │        │                                                         │
  │        │──< product_categories >── categories (self-ref parent) │
  │        │                                                         │
  │        │──< order_items >──< orders >── users (buyer_id)        │
  │        │                        │                               │
  │        │                        └──< notifications              │
  │        │                                                         │
  │        └──< reviews >── users (reviewer_id)                     │
  │                                                                  │
  └──< cart_items >──< products                                      │
                                                                     │
users ──────────────────────────────────────────────────────────────┘
```

---

## Tables

### `users`

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | UUID | PK | Internal UUID |
| `firebase_uid` | VARCHAR(128) | UNIQUE, NOT NULL | Firebase user UID |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | |
| `display_name` | VARCHAR(100) | | |
| `avatar_url` | TEXT | | |
| `phone` | VARCHAR(20) | | |
| `role` | ENUM | NOT NULL, DEFAULT 'buyer' | `buyer`, `seller`, `admin` |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Soft-disable account |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | |
| `updated_at` | TIMESTAMP | NOT NULL | Auto-updated |

### `categories`

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | PK, AUTOINCREMENT |
| `name` | VARCHAR(100) | NOT NULL, UNIQUE |
| `slug` | VARCHAR(100) | NOT NULL, UNIQUE |
| `parent_id` | INTEGER | FK → categories.id, NULLABLE |
| `created_at` | TIMESTAMP | NOT NULL |

### `products`

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | UUID | PK | |
| `seller_id` | UUID | FK → users.id, NOT NULL | |
| `category_id` | INTEGER | FK → categories.id | |
| `name` | VARCHAR(255) | NOT NULL | FTS indexed |
| `description` | TEXT | | FTS indexed |
| `price` | NUMERIC(12,2) | NOT NULL, CHECK > 0 | |
| `stock_quantity` | INTEGER | NOT NULL, DEFAULT 0, CHECK >= 0 | |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Soft-delete |
| `average_rating` | NUMERIC(3,2) | DEFAULT 0 | Denormalized, updated on review |
| `review_count` | INTEGER | DEFAULT 0 | Denormalized |
| `tags` | TEXT | | Comma-separated or JSON |
| `created_at` | TIMESTAMP | NOT NULL |
| `updated_at` | TIMESTAMP | NOT NULL |

### `product_images`

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | PK, AUTOINCREMENT |
| `product_id` | UUID | FK → products.id, CASCADE DELETE |
| `url` | TEXT | NOT NULL |
| `position` | INTEGER | NOT NULL, DEFAULT 0 |

### `cart_items`

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | PK, AUTOINCREMENT |
| `user_id` | UUID | FK → users.id, CASCADE DELETE |
| `product_id` | UUID | FK → products.id |
| `quantity` | INTEGER | NOT NULL, CHECK > 0 |
| `price_snapshot` | NUMERIC(12,2) | NOT NULL | Price at time of add |
| `added_at` | TIMESTAMP | NOT NULL |

**Unique constraint:** `(user_id, product_id)`

### `orders`

| Column | Type | Constraints |
|---|---|---|
| `id` | UUID | PK |
| `buyer_id` | UUID | FK → users.id, NOT NULL |
| `status` | ENUM | NOT NULL, DEFAULT 'pending' |
| `total_amount` | NUMERIC(12,2) | NOT NULL |
| `shipping_address` | TEXT | NOT NULL |
| `created_at` | TIMESTAMP | NOT NULL |
| `updated_at` | TIMESTAMP | NOT NULL |

**Order status enum:** `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`

### `order_items`

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | PK, AUTOINCREMENT |
| `order_id` | UUID | FK → orders.id, CASCADE DELETE |
| `product_id` | UUID | FK → products.id |
| `seller_id` | UUID | FK → users.id | Snapshot at order time |
| `quantity` | INTEGER | NOT NULL |
| `unit_price` | NUMERIC(12,2) | NOT NULL | Price snapshot |
| `subtotal` | NUMERIC(12,2) | NOT NULL | Computed: qty × unit_price |

### `reviews`

| Column | Type | Constraints |
|---|---|---|
| `id` | UUID | PK |
| `product_id` | UUID | FK → products.id, NOT NULL |
| `reviewer_id` | UUID | FK → users.id, NOT NULL |
| `order_id` | UUID | FK → orders.id, NOT NULL | Verified-purchase gate |
| `rating` | INTEGER | NOT NULL, CHECK 1–5 |
| `title` | VARCHAR(200) | |
| `body` | TEXT | |
| `is_flagged` | BOOLEAN | DEFAULT FALSE |
| `created_at` | TIMESTAMP | NOT NULL |

**Unique constraint:** `(product_id, reviewer_id)` — one review per buyer per product

### `notifications`

| Column | Type | Constraints |
|---|---|---|
| `id` | UUID | PK |
| `user_id` | UUID | FK → users.id, CASCADE DELETE |
| `type` | VARCHAR(50) | NOT NULL | e.g. `order_confirmed`, `order_shipped` |
| `title` | VARCHAR(200) | NOT NULL |
| `body` | TEXT | |
| `is_read` | BOOLEAN | DEFAULT FALSE |
| `reference_id` | UUID | NULLABLE | FK to related entity (order, review, etc.) |
| `created_at` | TIMESTAMP | NOT NULL |

---

## Indexes

```sql
-- Fast Firebase UID lookup on every authenticated request
CREATE UNIQUE INDEX ix_users_firebase_uid ON users(firebase_uid);

-- Product search and filtering
CREATE INDEX ix_products_seller_id ON products(seller_id);
CREATE INDEX ix_products_category_id ON products(category_id);
CREATE INDEX ix_products_is_active ON products(is_active);
CREATE INDEX ix_products_price ON products(price);

-- Full-text search (SQLite FTS5)
CREATE VIRTUAL TABLE products_fts USING fts5(
  name, description, content='products', content_rowid='rowid'
);

-- Cart
CREATE INDEX ix_cart_items_user_id ON cart_items(user_id);

-- Orders
CREATE INDEX ix_orders_buyer_id ON orders(buyer_id);
CREATE INDEX ix_orders_status ON orders(status);

-- Notifications
CREATE INDEX ix_notifications_user_id_is_read ON notifications(user_id, is_read);
```
