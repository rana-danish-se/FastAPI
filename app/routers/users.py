from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user as crud_create_user
from app.crud.user import get_users as crud_get_users
from app.database import get_db

router = APIRouter(tags=["Users"])

@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_create_user(db=db, user=user)

@router.get("/users", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_get_users(db, skip=skip, limit=limit)
    return users

