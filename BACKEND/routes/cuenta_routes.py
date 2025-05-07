from fastapi import APIRouter, Depends, Response, Request

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from schemas.cuenta_schema import CreateCuentaRequest, UpdateCuentaRequest, VerifyToken
from controllers import cuenta_controller
from database.finance import get_db
from controllers import cuenta_controller

router = APIRouter()

# obtener cuentas MEJORAR LO QUE RETORNA EL GET
@router.get("/account")
def get_cuentas(user=Depends(cuenta_controller.verify_token)):
    return {"msg": "Cuentas protegidas", "user_id": user["user_id"]}

# Ruta para crear una nueva cuenta de banco.
@router.post("/account")
def crear_cuenta( request: CreateCuentaRequest, db: Session = Depends(get_db), user: VerifyToken = Depends(cuenta_controller.verify_token)):
    if request.user_id != user.user_id:
        raise cuenta_controller.authorization_error()
    
    cuenta = cuenta_controller.crear_cuenta(request, db)
    return {"message": "Cuenta creada correctamente", "data": cuenta}

# Ruta para actualizar la información de la cuenta.
@router.patch("/account")
def update_cuenta(request: UpdateCuentaRequest, db: Session = Depends(get_db), user: VerifyToken = Depends(cuenta_controller.verify_token)):   
    cuenta = cuenta_controller.actualizar_cuenta(request, db, user.user_id)
    
    return {"msg":"Cuenta actualizada", "data": cuenta}