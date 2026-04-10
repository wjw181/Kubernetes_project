#存放数据模型
#接口输入输出的数据格式定义
from pydantic import BaseModel


class RootResponse(BaseModel):
    message: str
    docs: str
    health: str


class HealthResponse(BaseModel):
    status: str
    service: str
    env: str
    token_loaded: bool

class UserCreate(BaseModel):
    name: str
    age: int
    email: str


class User(UserCreate):
    id: int