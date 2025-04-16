from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
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

class TokenResponseFromAuthApi(BaseModel):
    access_token: str
    token_type: str