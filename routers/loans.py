from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, loans
from models import Loan, Book, User
from datetime import datetime

router = APIRouter()

# 대출 요청 엔드포인트
@router.post("/loans/borrow")
def borrow_book(book_id: int, user_id: int, db: Session = Depends(get_db)):
    # 도서 및 사용자 확인
    book = db.query(Book).filter(Book.id == book_id).first()
    user = db.query(User).filter(User.id == user_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if book.is_borrowed:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    # 대출 처리
    loan = Loan(book_id=book_id, user_id=user_id, borrowed_at=datetime.now())
    book.is_borrowed = True
    db.add(loan)
    db.commit()
    db.refresh(loan)

    return {"message": "Book borrowed successfully", "loan_id": loan.id}

# 반납 요청 엔드포인트
@router.post("/loans/return")
def return_book(loan_id: int, db: Session = Depends(get_db)):
    # 대출 기록 확인
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan record not found")

    # 반납 처리
    book = db.query(Book).filter(Book.id == loan.book_id).first()
    book.is_borrowed = False
    db.delete(loan)
    db.commit()

    return {"message": "Book returned successfully"}

# 대출 상태 조회 엔드포인트
@router.get("/loans")
def get_loans(user_id: int, db: Session = Depends(get_db)):
    loans = db.query(Loan).filter(Loan.user_id == user_id).all()
    return loans
