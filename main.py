from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

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

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"[DEBUG] Access token created for: {data['sub']}, Expires at: {expire}")
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        print(f"[DEBUG] Token verified for user: {username}")
        token_data = TokenData(username=username)
    except JWTError as e:
        print(f"[ERROR] Token verification failed: {e}")
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)

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
