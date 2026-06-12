"""Auth router - register and login endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", status_code=201)
def create_account(body: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(db, body.username, body.email, body.password)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create account: {e}")


@router.post("/login")
def login(body: UserLogin, db: Session = Depends(get_db)):
    try:
        return login_user(db, body.username, body.password)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {e}")
