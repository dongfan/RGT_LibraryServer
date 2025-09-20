
from fastapi import APIRouter, HTTPException
from typing import List
from models import Book
from database import books

router = APIRouter()

# CREATE
@router.post("/", response_model=Book)
def POST(book: Book):
    if book.isbn in books:
        raise HTTPException(status_code=400, detail="Book ISBN already exists")
    books[book.isbn] = book
    return book

# READ ALL
@router.get("/", response_model=List[Book])
def GET():
    return list(books.values())

# READ ONE
@router.get("/{isbn}", response_model=Book)
def GET_BY_ISBN(isbn: str):
    if isbn in books:
        return books[isbn]
    raise HTTPException(status_code=404, detail="Book not found")

# UPDATE
@router.put("/{isbn}", response_model=Book)
def PUT(isbn: str, updated_book: Book):
    if isbn in books:
        books[isbn] = updated_book
        return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# DELETE
@router.delete("/{isbn}", response_model=Book)
def DELETE(isbn: str):
    if isbn in books:
        return books.pop(isbn)
    raise HTTPException(status_code=404, detail="Book not found")
