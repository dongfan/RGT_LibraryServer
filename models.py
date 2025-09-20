from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

# 회원가입 데이터
class SignupData(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

# 로그인 데이터
class LoginData(BaseModel):
    username: str
    password: str

# User 모델 (DB 저장용)
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str  # 단순 저장, 나중에 해시 처리 가능
    full_name: Optional[str] = None

# Book 등록 데이터
class BookData(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    total_copies: int

# Book 모델 (DB 저장용)
class Book(BookData):
    id: int
    available_copies: int

# Loan 모델 (DB 저장용)
class Loan(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: date
    return_date: Optional[date] = None
