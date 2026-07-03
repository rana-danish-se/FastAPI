from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.post import Comment, CommentCreate, Post, PostCreate
from app.crud.post import create_post as crud_create_post
from app.crud.post import get_posts as crud_get_posts
from app.crud.post import get_post as crud_get_post
from app.crud.comment import create_comment as crud_create_comment
from app.crud.user import get_user as crud_get_user
from app.database import get_db

router = APIRouter(tags=["Posts", "Comments"])


@router.post("/posts", response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    author = crud_get_user(db, user_id=post.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    return crud_create_post(db=db, post=post)

@router.get("/posts", response_model=List[Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud_get_posts(db, skip=skip, limit=limit)
    return posts

@router.post("/posts/{post_id}/comments", response_model=Comment)
def add_comment(post_id: int, comment: CommentCreate, author_id: int, db: Session = Depends(get_db)):
    post = crud_get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    author = crud_get_user(db, user_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud_create_comment(db=db, comment=comment, post_id=post_id, author_id=author_id)
