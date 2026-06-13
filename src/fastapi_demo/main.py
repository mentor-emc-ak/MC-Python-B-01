from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="FastAPI Demo", description="A demo FastAPI app", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Static data ---

PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "category": "Electronics", "price": 99.99, "rating": 4.5, "in_stock": True},
    {"id": 2, "name": "Mechanical Keyboard", "category": "Electronics", "price": 149.99, "rating": 4.8, "in_stock": True},
    {"id": 3, "name": "Standing Desk Mat", "category": "Office", "price": 39.99, "rating": 4.3, "in_stock": False},
    {"id": 4, "name": "USB-C Hub", "category": "Electronics", "price": 59.99, "rating": 4.6, "in_stock": True},
    {"id": 5, "name": "Ergonomic Chair", "category": "Office", "price": 399.99, "rating": 4.7, "in_stock": True},
    {"id": 6, "name": "Webcam 4K", "category": "Electronics", "price": 129.99, "rating": 4.4, "in_stock": True},
]

TEAM = [
    {"id": 1, "name": "Aria Chen", "role": "Lead Engineer", "location": "San Francisco", "skills": ["Python", "FastAPI", "PostgreSQL"]},
    {"id": 2, "name": "Marcus Webb", "role": "Frontend Developer", "location": "Austin", "skills": ["React", "TypeScript", "Tailwind"]},
    {"id": 3, "name": "Priya Nair", "role": "DevOps Engineer", "location": "Remote", "skills": ["Docker", "Kubernetes", "CI/CD"]},
]

STATS = {
    "total_products": len(PRODUCTS),
    "in_stock": sum(1 for p in PRODUCTS if p["in_stock"]),
    "categories": list({p["category"] for p in PRODUCTS}),
    "team_size": len(TEAM),
}


# --- HTML routes ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "stats": STATS})


@app.get("/products", response_class=HTMLResponse)
async def products_page(request: Request):
    return templates.TemplateResponse("products.html", {"request": request, "products": PRODUCTS})


@app.get("/team", response_class=HTMLResponse)
async def team_page(request: Request):
    return templates.TemplateResponse("team.html", {"request": request, "team": TEAM})


# --- JSON API routes ---

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "fastapi-demo", "version": "1.0.0"}


@app.get("/api/stats")
async def stats():
    return STATS


@app.get("/api/products")
async def get_products():
    return {"products": PRODUCTS, "total": len(PRODUCTS)}


@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/api/team")
async def get_team():
    return {"team": TEAM, "total": len(TEAM)}
