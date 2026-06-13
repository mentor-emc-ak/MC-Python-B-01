from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import database
import models

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Todo App", description="SQLAlchemy + SQLite Todo API", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# --- Schemas ---

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=1000)
    priority: str = Field("medium", pattern="^(low|medium|high)$")


def _serialize(todo: models.Todo) -> dict:
    return {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "priority": todo.priority,
        "completed": todo.completed,
        "created_at": todo.created_at.isoformat() if todo.created_at else None,
    }


# --- HTML ---

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# --- JSON API ---

@app.get("/api/todos")
def list_todos(db: Session = Depends(database.get_db)):
    todos = (
        db.query(models.Todo)
        .order_by(models.Todo.completed.asc(), models.Todo.created_at.desc())
        .all()
    )
    return [_serialize(t) for t in todos]


@app.post("/api/todos", status_code=status.HTTP_201_CREATED)
def create_todo(body: TodoCreate, db: Session = Depends(database.get_db)):
    todo = models.Todo(
        title=body.title,
        description=body.description,
        priority=body.priority,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return _serialize(todo)


@app.patch("/api/todos/{todo_id}/toggle")
def toggle_todo(todo_id: int, db: Session = Depends(database.get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = not todo.completed
    db.commit()
    db.refresh(todo)
    return _serialize(todo)


@app.delete("/api/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(database.get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()


@app.get("/api/stats")
def stats(db: Session = Depends(database.get_db)):
    total = db.query(models.Todo).count()
    done = db.query(models.Todo).filter(models.Todo.completed == True).count()
    return {"total": total, "completed": done, "active": total - done}


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "todo-app", "version": "1.0.0"}
