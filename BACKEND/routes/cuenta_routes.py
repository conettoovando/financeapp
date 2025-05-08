from fastapi import APIRouter, Depends, Response, Request

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from schemas.cuenta_schema import CreateCuentaRequest, UpdateCuentaRequest, VerifyToken, DeleteCuentaRequest
from controllers import cuenta_controller
from database.finance import get_db
from controllers import cuenta_controller

router = APIRouter(prefix="/account")

# obtener cuentas MEJORAR LO QUE RETORNA EL GET
@router.get("")
def get_cuentas(db: Session = Depends(get_db), user: VerifyToken = Depends(cuenta_controller.verify_token)):
    return cuenta_controller.obtener_cuentas(db, user.user_id)

# Ruta para crear una nueva cuenta de banco.
@router.post("")
def crear_cuenta( request: CreateCuentaRequest, db: Session = Depends(get_db), user: VerifyToken = Depends(cuenta_controller.verify_token)):
    if request.user_id != user.user_id:
        raise cuenta_controller.authorization_error()
    
    cuenta = cuenta_controller.crear_cuenta(request, db)
    return {"message": "Cuenta creada correctamente", "data": cuenta}

# Ruta para actualizar la información de la cuenta.
@router.patch("")
def update_cuenta(request: UpdateCuentaRequest, db: Session = Depends(get_db), user: VerifyToken = Depends(cuenta_controller.verify_token)):   
    cuenta = cuenta_controller.actualizar_cuenta(request, db, user.user_id)
    
    return {"msg":"Cuenta actualizada", "data": cuenta}

@router.delete("")
def delete_cuenta(request: DeleteCuentaRequest, db: Session = Depends(get_db), user: VerifyToken = Depends(cuenta_controller.verify_token)):
    return cuenta_controller.eliminar_cuenta(request, db, user.user_id)