from fastapi import APIRouter, Depends, Response, Request

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from schemas.cuenta_schema import CreateCuentaRequest
from controllers import cuenta_controller
from schemas.user_schema import UserCreate, UserLogin
from database.finance import get_db
from controllers import cuenta_controller

router = APIRouter(prefix="/account", tags=["accounts"])

@router.get("/")
def get_cuentas(user=Depends(cuenta_controller.verify_token)):
    return {"msg": "Cuentas protegidas", "user_id": user["user_id"]}

@router.post("/crear-cuenta")
def crear_cuenta( request: CreateCuentaRequest, db: Session = Depends(get_db), user=Depends(cuenta_controller.verify_token)):
    if request.user_id != user["user_id"]:
        raise HTTPException(status_code=400, detail="Usuario no autorizado")
    
    cuenta = cuenta_controller.crear_cuenta(request, db)
    return {"message": "Cuenta creada correctamente", "data": cuenta}