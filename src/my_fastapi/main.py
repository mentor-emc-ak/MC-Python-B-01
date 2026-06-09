from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class TodoBody(BaseModel):
    title: str
    description: str


my_todos = {
    "1": {"title": "Buy groceries", "description": "Milk, Bread, Eggs"},
    "2": {"title": "Read a book", "description": "The Great Gatsby"},
    "3": {"title": "Go for a walk", "description": "30 minutes in the park"}
}

@app.get("/")
def read_root():
    return {"message": "The Server is up and running!"}

@app.get("/todos")
def read_todos():
    return {"todos": list(my_todos.values())}

@app.get("/todos/{todo_id}")
def read_todo(todo_id: str):
    todo = my_todos.get(todo_id)
    if todo:
        return {"todo": todo}
    else:
        return {"error": "Todo not found"}

@app.post("/todos")
def create_todo(body: TodoBody):
    todo_id = str(len(my_todos) + 1)
    if todo_id in my_todos:
        return {"error": "Todo ID already exists"}
    my_todos[todo_id] = {"title": body.title, "description": body.description}
    return {"message": "Todo created successfully", "todo": my_todos[todo_id]}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: str, body: TodoBody):
    if todo_id in my_todos:
        my_todos[todo_id] = {"title": body.title, "description": body.description, "completed": body.completed}
        return {"message": "Todo updated successfully", "todo": my_todos[todo_id]}
    else:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    if todo_id in my_todos:
        del my_todos[todo_id]
        return {"message": "Todo deleted successfully"}
    else:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
