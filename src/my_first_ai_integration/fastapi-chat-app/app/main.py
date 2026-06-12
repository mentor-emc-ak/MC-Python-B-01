"""FastAPI AI Chat Application — entry point."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.models.database import init_db
from app.routers import auth, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI Chat Application",
    description="FastAPI + SQLite + OpenAI. Register, login, and chat with AI.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)

# Serve frontend static files
_static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=_static_dir), name="static")


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "db": "sqlite (chat_app.db)",
        "ai_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
    }


@app.get("/{full_path:path}", include_in_schema=False)
def spa_fallback(full_path: str):
    """Catch-all: serve the SPA for any non-API route."""
    return FileResponse(os.path.join(_static_dir, "index.html"))


if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 55)
    print("  AI Chat Application")
    print("=" * 55)
    print("  App:        http://localhost:8000")
    print("  API Docs:   http://localhost:8000/docs")
    print(f"  OpenAI Key: {'Set' if os.getenv('OPENAI_API_KEY') else 'NOT SET — add to .env'}")
    print("=" * 55 + "\n")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
