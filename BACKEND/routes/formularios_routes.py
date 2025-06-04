from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from schemas.user_schema import VerifyToken
from controllers import formularios_controller
from database.finance import get_db
from controllers import user_controller
from schemas.formularios_schema import CreateCuentaResponse


router = APIRouter()

@router.get("/createCuenta", response_model=CreateCuentaResponse)
async def crear_cuentas(
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token)
):
    if user:
        return formularios_controller.crearCuenta(db, user.user_id)
    
    raise HTTPException(status_code=401, detail="Acceso no autorizado")