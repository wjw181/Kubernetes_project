#存放用户相关接口

from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from schemas import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

# 模拟数据库
users_db: List[User] = [
    User(id=1, name="Alice", age=22, email="alice@example.com"),
    User(id=2, name="Bob", age=24, email="bob@example.com"),
]


@router.get("/", response_model=List[User])
def get_users():
    return users_db


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate):
    new_id = max([u.id for u in users_db], default=0) + 1
    new_user = User(id=new_id, **user.model_dump())
    users_db.append(new_user)
    return new_user