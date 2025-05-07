from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: Optional[str] = None
    email: EmailStr

class UserCreate(UserBase):
    email: EmailStr
    password: str

class User(UserBase):
    id: str
    created_at: Optional[datetime] 
    updated_at: Optional[datetime]

    class config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserDelete(BaseModel):
    email: EmailStr
    password: str