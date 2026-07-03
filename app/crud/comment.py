from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.post import CommentCreate

def get_comments_for_post(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: CommentCreate, post_id: int, author_id: int):
    db_comment = Comment(
        text=comment.text,
        post_id=post_id,
        author_id=author_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
