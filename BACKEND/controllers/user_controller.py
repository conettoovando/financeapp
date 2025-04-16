from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from models.user import Users
from schemas.user import UserCreate, UserLogin
from sqlalchemy import text
import requests
import json

AUTH_URL = "http://localhost:5173"

def create_user(db: Session, user: UserCreate):

    credenciales = requests.post(AUTH_URL+"/register", json=user.model_dump())

    cred_json = credenciales.json()

    db_user = Users(
        id = cred_json["id"]
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def login_user(db: Session, user: UserLogin):
    res = requests.post(AUTH_URL+"/login", json = user.model_dump())

    if res.status_code != 200:
        return None

    data = res.json()

    return {
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "token_type": data["token_type"]
    }
    