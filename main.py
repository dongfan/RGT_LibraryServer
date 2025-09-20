from fastapi import FastAPI, Depends, HTTPException
from routers.auth import create_access_token, verify_token
from utils.validation import validate_password_strength
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
import re

load_dotenv()

app = FastAPI()

# -----------------------
# 데이터 모델 정의
# -----------------------
class SignupData(BaseModel):
    username: str
    email: EmailStr  # 이메일 형식 검증을 위해 EmailStr 사용
    password: str
    full_name: str

class LoginData(BaseModel):
    username: str
    password: str

class BookData(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    total_copies: int

# JWT 설정
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)

def validate_password_strength(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter")
    if not re.search(r"[0-9]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one digit")

# -----------------------
# 임시 데이터베이스 (메모리, dict 기반)
# -----------------------
users_db = {}
books_db = {}

# -----------------------
# 엔드포인트 구현
# -----------------------

@app.post("/auth/signup")
def signup(data: SignupData):
    # 이메일 형식은 Pydantic의 EmailStr이 자동으로 검증합니다.

    # 비밀번호 강도 검증
    validate_password_strength(data.password)

    # 이미 존재하는 username 체크
    for user in users_db.values():
        if user["username"] == data.username:
            raise HTTPException(status_code=400, detail="Username already exists")
    user_id = len(users_db) + 1
    user_dict = data.dict()
    user_dict["id"] = user_id
    print("저장되는 데이터:", user_dict)
    users_db[user_id] = user_dict
    return {"message": "User registered successfully", "user": data.username}


@app.post("/auth/login", response_model=Token)
def login(data: LoginData):
    user = next((u for u in users_db.values() if u["username"] == data.username and u["password"] == data.password), None)
    if not user:
        print(f"[ERROR] Login failed for username: {data.username}")
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    print(f"[DEBUG] Login successful for username: {data.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/books", tags=["Books"])
def add_book(data: BookData):
    if data.isbn in books_db:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    book_id = len(books_db) + 1
    book_dict = data.dict()
    book_dict["id"] = book_id
    books_db[data.isbn] = book_dict
    return {"message": "Book added successfully", "book": data.title}

@app.get("/books", tags=["Books"])
def get_books():
    return {"books": list(books_db.values())}


@app.delete("/books/{isbn}", tags=["Books"])
def delete_book(isbn: str):
    if isbn in books_db:
        books_db.pop(isbn)
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/protected-route")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}
