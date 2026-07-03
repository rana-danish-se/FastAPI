from fastapi import FastAPI

from app.routers.posts import router as posts_router
from app.routers.users import router as users_router
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Learning API",
    description="An API for managing Users, Posts, and Comments",
    version="1.0.0"
)

app.include_router(users_router)
app.include_router(posts_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Learning API!"}