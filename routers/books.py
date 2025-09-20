from fastapi import APIRouter, HTTPException
from typing import List
from models import Book
from database import books

router = APIRouter()

# CREATE
@router.post("/", response_model=Book)
def POST(book: Book):
    if any(b.id == book.id for b in books):
        raise HTTPException(status_code=400, detail="Book ID already exists")
    books.append(book)
    return book

# READ ALL
@router.get("/", response_model=List[Book])
def GET():
    return books

# READ ONE
@router.get("/{book_id}", response_model=Book)
def GET_BY_ID(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# UPDATE
@router.put("/{book_id}", response_model=Book)
def PUT(book_id: int, updated_book: Book):
    for i, book in enumerate(books):
        if book.id == book_id:
            books[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# DELETE
@router.delete("/{book_id}", response_model=Book)
def DELETE(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            return books.pop(i)
    raise HTTPException(status_code=404, detail="Book not found")
