from fastapi import FastAPI

from app.routers.books import router as books_router
from app.routers.posts import router as posts_router
from app.routers.users import router as users_router

app = FastAPI(
    title="Bookstore API",
    description="An API for managing a bookstore and its learning of Day 01",
    version="1.0.0"
)

app.include_router(books_router)
app.include_router(users_router)
app.include_router(posts_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Bookstore API!"}