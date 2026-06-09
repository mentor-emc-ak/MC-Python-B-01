from sqlalchemy.orm import Session
import bcrypt

from models import Todo, User
from schemas import TodoCreate, TodoUpdate, UserCreate, UserUpdate


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


# --- User ---

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User | None:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    updates = user_data.model_dump(exclude_unset=True)
    if "password" in updates:
        updates["password"] = hash_password(updates["password"])
    for field, value in updates.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True


# --- Todo ---

def get_todo(db: Session, todo_id: int) -> Todo | None:
    return db.query(Todo).filter(Todo.id == todo_id).first()


def get_todos_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Todo]:
    return db.query(Todo).filter(Todo.user_id == user_id).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: TodoCreate, user_id: int) -> Todo:
    db_todo = Todo(**todo.model_dump(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo_data: TodoUpdate) -> Todo | None:
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    for field, value in todo_data.model_dump(exclude_unset=True).items():
        setattr(db_todo, field, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> bool:
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return False
    db.delete(db_todo)
    db.commit()
    return True
