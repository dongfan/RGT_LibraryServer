from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# Secret key and algorithm for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"[DEBUG] Access token created for user: {data['sub']} with expiration: {expire}")
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        print(f"[DEBUG] Verifying token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        print(f"[DEBUG] Token verified for user: {username}")
        return username
    except JWTError as e:
        print(f"[ERROR] Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")