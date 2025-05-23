from fastapi import Request
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from models.user import Users
from schemas.user_schema import VerifyToken
from schemas.user_schema import UserCreate, UserLogin
import requests
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

AUTH_URL = os.getenv("auth_url")

AUTH_PUBLIC_KEY_URL = "http://localhost:8000/auth/public-key"
ALGORITHM="RS256"

def get_public_key():
    res = requests.get(AUTH_PUBLIC_KEY_URL)
    if res.status_code != 200:
        raise RuntimeError("No se pudo obtener la clave pública")
    return res.text

def verify_token(request: Request) -> VerifyToken:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    try:
        payload = jwt.decode(token, public_key, algorithms=ALGORITHM)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token sin 'sub'")
        
        return VerifyToken(
            user_id=user_id
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")

public_key = get_public_key()

def create_user(db: Session, user: UserCreate):
    try:
        response = requests.post(AUTH_URL+"/register", json=user.model_dump())

        if response.status_code != 201:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Error al registrar usuario")
            )

        cred_json = response.json()

        db_user = Users(
            id = cred_json["id"]
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {
            "detail": "Usuario creado correctamente"
        }
    
    except requests.RequestException as error:
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo conectar con el microservicio de autenticación: {str(error)}"
        )   

def login_user(db: Session, user: UserLogin):
    res = requests.post(AUTH_URL+"/login", json = user.model_dump())

    if res.status_code != 200:
        return None

    data: dict = res.json()

    return_data = {
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "token_type": data["token_type"]
    }

    if data.get("id"):
        print("verificando registro")
        user_in_db = db.query(Users).filter_by(id=data["id"]).first()

        if not user_in_db:
            print("Creando usuario")
            new_user = Users(id=data["id"])
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

    return return_data

def me(request: Request):
    token = request.cookies.get("access_token")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{AUTH_URL}/me", headers=headers)

    if response.status_code == 200:
        return response.json()
    
    return {"error": "Token invalido o expirado"}

def refresh_token(token: str):
    response = requests.post(
        f"{AUTH_URL}/refresh",
        json={"refresh_token": token}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Token de refresco invalido")
    
    return response.json()