
from fastapi import APIRouter, HTTPException
from typing import List
from models import User
from database import users

router = APIRouter()

# CREATE
@router.post("/", response_model=User)
def POST(user: User):
    if user.id in users:
        raise HTTPException(status_code=400, detail="User ID already exists")
    users[user.id] = user
    return user

# READ ALL
@router.get("/", response_model=List[User])
def GET():
    return list(users.values())

# READ ONE
@router.get("/{user_id}", response_model=User)
def GET_BY_ID(user_id: int):
    if user_id in users:
        return users[user_id]
    raise HTTPException(status_code=404, detail="User not found")

# UPDATE
@router.put("/{user_id}", response_model=User)
def PUT(user_id: int, updated_user: User):
    if user_id in users:
        users[user_id] = updated_user
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# DELETE
@router.delete("/{user_id}", response_model=User)
def DELETE(user_id: int):
    if user_id in users:
        return users.pop(user_id)
    raise HTTPException(status_code=404, detail="User not found")
