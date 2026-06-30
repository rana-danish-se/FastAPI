from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Bookstore API",
    description="An API for managing a bookstore and its learning of Day 02",
    version="1.0.0"
)

users = []
posts = []

user_id_counter = 1
post_id_counter = 1
comment_id_counter = 1


# ---------- USER ----------
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


# ---------- COMMENT ----------
class CommentCreate(BaseModel):
    text: str = Field(..., min_length=3)

class Comment(CommentCreate):
    id: int
    author: UserOut
    created_at: datetime


# ---------- POST ----------
class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    subtitle: Optional[str] = Field(None, max_length=200)
    body: str = Field(..., min_length=1)
    author_id: int   # client tells us which user is the author


class Post(PostCreate):
    id: int
    author: UserOut
    created_at: datetime
    comments: List[Comment] = []


# ---------- ROUTES ----------
@app.post("/users", response_model=UserOut, tags=["Users"])
def create_user(user: UserCreate):
    global user_id_counter
    new_user = User(id=user_id_counter, **user.dict(), is_active=True)
    user_id_counter += 1
    users.append(new_user)
    return new_user


@app.post("/posts", response_model=Post, tags=["Posts"])
def create_post(post: PostCreate):
    global post_id_counter

    author = next((u for u in users if u.id == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_post = Post(
        id=post_id_counter,
        title=post.title,
        subtitle=post.subtitle,
        body=post.body,
        author_id=post.author_id,
        author=author,
        created_at=datetime.now(),
        comments=[]
    )
    post_id_counter += 1
    posts.append(new_post)
    return new_post


@app.post("/posts/{post_id}/comments", response_model=Comment, tags=["Comments"])
def add_comment(post_id: int, comment: CommentCreate, author_id: int):
    global comment_id_counter

    post = next((p for p in posts if p.id == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    author = next((u for u in users if u.id == author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_comment = Comment(
        id=comment_id_counter,
        text=comment.text,
        author=author,
        created_at=datetime.now()
    )
    comment_id_counter += 1
    post.comments.append(new_comment)
    return new_comment