from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.post import Comment, CommentCreate, Post, PostCreate
from app.schemas.user import UserOut
from app.routers.users import users

router = APIRouter(tags=["Posts", "Comments"])
posts = []
post_id_counter = 1
comment_id_counter = 1


@router.post("/posts", response_model=Post)
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


@router.post("/posts/{post_id}/comments", response_model=Comment)
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
