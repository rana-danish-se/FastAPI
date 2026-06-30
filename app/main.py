from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI(
    title="Bookstore API",
    description="An API for managing a bookstore and its learning of Day 01",
    version="1.0.0"
)
books=[]

class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float
    available: bool
    
    model_config={
        "json_schema_extra":{
            "example": {
                "id": 1,
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "price": 10.99,
                "available": True
                
            }
        }
    }



@app.get("/")
def read_root():
    return {"message": "Welcome to the Bookstore API!"}

@app.get("/books", tags=["Books"])
def get_books(skip: int = 0, limit: int = 10):
    return books[skip: skip + limit]

@app.get("/books/{book_id}", tags=["Books"])
def get_book(book_id:int):
    for book in books:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}

@app.post("/books", tags=["Books"])
def create_book(book:Book):
    books.append(book)
    return book

@app.put("/books/{book_id}", tags=["Books"])
def update_book(book_id:int, updated_book:Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = updated_book
            return updated_book
    return {"error": "Book not found"}

@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id:int):
    for index, book in enumerate(books):
        if book.id == book_id:
            deleted_book = books.pop(index)
            return deleted_book
    return {"error": "Book not found"}