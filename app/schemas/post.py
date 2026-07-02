from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .user import UserOut


class CommentCreate(BaseModel):
    text: str = Field(..., min_length=3)


class Comment(CommentCreate):
    id: int
    author: UserOut
    created_at: datetime


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    subtitle: Optional[str] = Field(None, max_length=200)
    body: str = Field(..., min_length=1)
    author_id: int


class Post(PostCreate):
    id: int
    author: UserOut
    created_at: datetime
    comments: List[Comment] = []
