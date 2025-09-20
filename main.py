from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# -----------------------
# 데이터 모델 정의
# -----------------------
class SignupData(BaseModel):
    username: str
    email: str
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

# -----------------------
# 임시 데이터베이스 (메모리)
# -----------------------
users_db = []
books_db = []

# -----------------------
# 엔드포인트 구현
# -----------------------

@app.post("/auth/signup")
def signup(data: SignupData):
    # 이미 존재하는 username 체크
    for user in users_db:
        if user["username"] == data.username:
            raise HTTPException(status_code=400, detail="Username already exists")
    user_dict = data.dict()
    print("저장되는 데이터:", user_dict)
    users_db.append(data.dict())
    return {"message": "User registered successfully", "user": data.username}


@app.post("/auth/login")
def login(data: LoginData):
    for user in users_db:
        if user["username"] == data.username and user["password"] == data.password:
            return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")


@app.post("/books")
def add_book(data: BookData):
    for book in books_db:
        if book["isbn"] == data.isbn:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    books_db.append(data.dict())
    return {"message": "Book added successfully", "book": data.title}

@app.get("/users")
def get_users():
    return {"users": users_db}

@app.get("/books")
def get_books():
    return {"books": books_db}


@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    for book in books_db:
        if book["isbn"] == isbn:
            books_db.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
