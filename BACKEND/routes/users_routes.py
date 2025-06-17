from fastapi import APIRouter, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordBearer

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from controllers import user_controller
from schemas.user_schema import UserCreate, UserLogin, UserLoginBody, VerifyToken
from database.finance import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register")
async def create_account(account: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db, account)

@router.post("/login")
async def login_account(user_id: UserLoginBody, db: Session = Depends(get_db)):
    print("user_id", user_id.user_id)
    return user_controller.login_user(db, user_id.user_id)

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

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def cerrar_session(response: Response):
    cookie_settings = {
        "httponly": True,
        "secure": True,
        "samesite": "none",
        "path": "/",  # opcional si lo usaste en set_cookie
    }

    response.delete_cookie("access_token", **cookie_settings)
    response.delete_cookie("refresh_token", **cookie_settings)
    
    # token_type era httponly=False, así que debe ir separado
    response.delete_cookie("token_type", secure=True, samesite="none", path="/")

    return {"message": "Sesión cerrada"}