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
# 임시 데이터베이스 (메모리, dict 기반)
# -----------------------
users_db = {}
books_db = {}

# -----------------------
# 엔드포인트 구현
# -----------------------

@app.post("/auth/signup")
def signup(data: SignupData):
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


@app.post("/auth/login")
def login(data: LoginData):
    for user in users_db.values():
        if user["username"] == data.username and user["password"] == data.password:
            return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")


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
