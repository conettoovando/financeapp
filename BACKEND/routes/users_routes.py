from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from controllers import user_controller
from schemas.user_schema import UserCreate, UserLogin
from database.finance import get_db

router = APIRouter(prefix="/auth", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register")
async def create_account(account: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db, account)

@router.post("/login")
async def login_account(account: UserLogin, db: Session = Depends(get_db), response: Response = Response()):
    tokens = user_controller.login_user(db, account)

    if not tokens:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24 * 7
    )

    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=True,
        samesite="none"
    )

    response.set_cookie(
        key="token_type",
        value=tokens["token_type"],
        httponly=False,
        secure=True,
        samesite="none"
    )

    return {"msg": "Acceso consedido con exito"}

@router.post("/refresh")
async def refresh_tokens(request: Request, response: Response = Response()):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Token de refresco no encontrado")
    
    token = user_controller.refresh_token(token=refresh_token)

    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24 * 7
    )

    return {"msg": "Token de acceso actualizado"}

@router.get("/me")
async def me(request: Request):
    return user_controller.me(request)

@router.put("/me")
async def actualizar_usuario():
    pass

@router.delete("/me")
async def eliminar_usuario():
    pass
