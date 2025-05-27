from fastapi import Request, Response
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
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token sin 'id'")
        
        return VerifyToken(
            user_id=user_id
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")

public_key = get_public_key()

def create_user(db: Session, user: UserCreate):
    if AUTH_URL:
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
    raise HTTPException(
        status_code=500,
        detail="Error interno del servidor"
    )

def login_user(db: Session, user_id: str):
    if user_id:
        user_in_db = db.get(Users, user_id)

        if not user_in_db:
            new_user = Users(id=user_id)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {"sucess", "registrado correctamente"}

        raise HTTPException(status_code=400, detail="Usuario ya registrado")

def me(request: Request):
    token = request.cookies.get("access_token")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{AUTH_URL}/me", headers=headers)

    if response.status_code == 200:
        return response.json()
    
    raise HTTPException(status_code=response.status_code, detail="Token invalido o expirado")

def refresh_token(token: str):
    response = requests.post(
        f"{AUTH_URL}/refresh",
        json={"refresh_token": token}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Token de refresco invalido")
    
    return response.json()