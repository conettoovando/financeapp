from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from models.user import Users
from schemas.user import UserCreate, UserRead, UserLogin, JwtResponse
import uuid
import bcrypt
import jwt
from sqlalchemy import text
from datetime import datetime, timedelta, timezone
from cryptography.hazmat.primitives import serialization
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

PRIVATE_KEY_PATH = Path(os.getenv("PRIVATE_KEY_PATH"))
PUBLIC_KEY_PATH = Path(os.getenv("PUBLIC_KEY_PATH"))
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_user(db: Session, user: UserCreate):
    new_id = db.execute(text("SELECT UUID_TO_BIN(UUID())")).scalar()

    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = Users(
        id=new_id,
        name=user.name,
        email=user.email,
        password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserRead(
        id=str(uuid.UUID(bytes=db_user.id)),
        name=db_user.name,
        email=db_user.email,
    )

def login_user(db: Session, user: UserLogin):
    
    db_user = get_user_by_email(db, user.email)

    if db_user is None or not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    
    # Incorporar JWT
    payload = {
        "sub": str(uuid.UUID(bytes=db_user.id)),
        "name": db_user.name,
        "email": db_user.email
    }

    access_token = create_access_token(
        data=payload,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_access_token(
        data=payload,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return JwtResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )

def refresh_token(token: str):
    try:
        payload = verify_token(token)

        new_access_token = create_access_token(
            {"sub": payload["sub"], "email": payload["email"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return JwtResponse(
            access_token=new_access_token,
            refresh_token=token
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expirado")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Refresh token invalido")
    
def verify_user(token: str):
    try:
        user = verify_token(token)
        return {"msg": "Token valido", "user": user, "token": token}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalido")

def get_user_by_email(db: Session, email:str):
    return db.query(Users).filter(Users.email == email).first()


def load_private_key():
    with open(PRIVATE_KEY_PATH, 'r') as file:
        return serialization.load_ssh_private_key(file.read().encode(), password=b'')

def load_public_key():
    with open(PUBLIC_KEY_PATH, 'r') as file:
        return serialization.load_ssh_public_key(file.read().encode())

def create_access_token(data: dict, expires_delta: timedelta):
    key = load_private_key()

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, key=key, algorithm='RS256')
    
    return encoded_jwt

def verify_token(token: str):
    try:
        key = load_public_key()
        token = jwt.decode(token, key=key, algorithms=["RS256"], options={"verify_exp": True})

        return token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido")