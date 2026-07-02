from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)


class User(UserCreate):
    id: int
    is_active: bool = True


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True
