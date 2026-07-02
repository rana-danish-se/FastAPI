from fastapi import APIRouter, HTTPException

from app.schemas.user import User, UserCreate, UserOut

router = APIRouter(tags=["Users"])
users = []
user_id_counter = 1


@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate):
    global user_id_counter
    new_user = User(id=user_id_counter, **user.model_dump(), is_active=True)
    user_id_counter += 1
    users.append(new_user)
    return new_user
