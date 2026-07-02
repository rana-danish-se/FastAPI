from fastapi import APIRouter

from app.schemas.book import Book

router = APIRouter(prefix="/books", tags=["Books"])
books = []


@router.get("")
def get_books(skip: int = 0, limit: int = 10):
    return books[skip: skip + limit]


@router.get("/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}


@router.post("", response_model=Book)
def create_book(book: Book):
    books.append(book)
    return book


@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = updated_book
            return updated_book
    return {"error": "Book not found"}


@router.delete("/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            deleted_book = books.pop(index)
            return deleted_book
    return {"error": "Book not found"}
