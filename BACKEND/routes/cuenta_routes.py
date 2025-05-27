from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from schemas.cuenta_schema import (
    CreateCuentaRequest, 
    UpdateCuentaRequest,  
    DeleteCuentaRequest, 
    GetCuetasResponse
)
from schemas.user_schema import VerifyToken
from controllers import cuenta_controller
from database.finance import get_db
from controllers import user_controller

router = APIRouter()

# obtener cuentas MEJORAR LO QUE RETORNA EL GET
@router.get("/{cuenta_id}", response_model=GetCuetasResponse)
def obtener_cuenta(
        cuenta_id: str,
        db: Session = Depends(get_db),
        user: VerifyToken = Depends(user_controller.verify_token)
    ):
    return cuenta_controller.obtener_cuenta(db, user.user_id, cuenta_id)

@router.get("", response_model=List[GetCuetasResponse], response_model_exclude_none=True)
def get_cuentas(
        db: Session = Depends(get_db),
        user: VerifyToken = Depends(user_controller.verify_token)
    ):
    return cuenta_controller.obtener_cuentas(db, user.user_id)

# Ruta para crear una nueva cuenta de banco.
@router.post("")
def crear_cuenta( request: CreateCuentaRequest, db: Session = Depends(get_db), user: VerifyToken = Depends(user_controller.verify_token)):
    if request.user_id != user.user_id:
        raise cuenta_controller.authorization_error()
    
    cuenta = cuenta_controller.crear_cuenta(request, db)
    return {"message": "Cuenta creada correctamente", "data": cuenta}

# Ruta para actualizar la información de la cuenta.
@router.patch("")
def update_cuenta(request: UpdateCuentaRequest, db: Session = Depends(get_db), user: VerifyToken = Depends(user_controller.verify_token)):   
    cuenta = cuenta_controller.actualizar_cuenta(request, db, user.user_id)
    
    return {"msg":"Cuenta actualizada", "data": cuenta}

@router.delete("")
def delete_cuenta(request: DeleteCuentaRequest, db: Session = Depends(get_db), user: VerifyToken = Depends(user_controller.verify_token)):
    return cuenta_controller.eliminar_cuenta(request, db, user.user_id)