from fastapi import APIRouter, HTTPException
from typing import List
from models import User
from database import users

router = APIRouter()

# CREATE
@router.post("/", response_model=User)
def POST(user: User):
    if any(u.id == user.id for u in users):
        raise HTTPException(status_code=400, detail="User ID already exists")
    users.append(user)
    return user

# READ ALL
@router.get("/", response_model=List[User])
def GET():
    return users

# READ ONE
@router.get("/{user_id}", response_model=User)
def GET_BY_ID(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# UPDATE
@router.put("/{user_id}", response_model=User)
def PUT(user_id: int, updated_user: User):
    for i, user in enumerate(users):
        if user.id == user_id:
            users[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# DELETE
@router.delete("/{user_id}", response_model=User)
def DELETE(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail="User not found")
