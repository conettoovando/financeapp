from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from controllers import user_controller
from schemas.user import UserCreate, UserRead, UserLogin, JwtResponse, RefreshToken
from database.user import get_db

router = APIRouter(prefix="/auth", tags=["accounts"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/me")
async def get_user(token: str = Depends(oauth2_scheme)):
    return user_controller.verify_user(token=token)

@router.post("/register", response_model=UserRead)
async def create_account(account: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db, account)

@router.post("/login", response_model=JwtResponse)
async def login_account(account: UserLogin, db: Session = Depends(get_db)):
    return user_controller.login_user(db, account)

@router.post('/refresh')
async def refresh_token(refresh_token: RefreshToken):
    return user_controller.refresh_token(token = refresh_token.refresh_token)
