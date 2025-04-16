from fastapi import APIRouter, Depends, Response
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from controllers import user_controller
from schemas.user import UserCreate, UserLogin, TokenResponseFromAuthApi
from database.user import get_db

router = APIRouter(prefix="/auth", tags=["accounts"])

@router.post("/register")
async def create_account(account: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db, account)

@router.post("/login", response_model=TokenResponseFromAuthApi)
async def login_account(account: UserLogin, db: Session = Depends(get_db), response: Response = Response()):
    tokens = user_controller.login_user(db, account)

    if not tokens:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict"
    )

    return {
        "access_token": tokens["access_token"],
        "token_type": tokens["token_type"]
    }