from fastapi import APIRouter, Depends, Query, Request
from typing import List, Optional

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from schemas.movimientos_schema import (
    CreateNewMovimiento,
    NuevoMovimientoResponse,
    ObtenerMovimientos,
    MovimientoModel,
    ActualizarMovimiento
)
from schemas.user_schema import VerifyToken
from database.finance import get_db
from controllers import movimiento_controller
from controllers import user_controller

router = APIRouter()

@router.get("/", response_model=ObtenerMovimientos)
async def obtener_movimientos(
    request: Request,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token),
    limit: int = 10,
    offset: int = 0,
    orden: str = "desc",
    cuenta_id: Optional[str] = None  # 🆕
):
    base_url = str(request.url.replace(query=None))
    return movimiento_controller.obtener_movimientos(
        db, user.user_id, limit, offset, orden, base_url, cuenta_id
    )



@router.get("/{mov_id}", response_model=MovimientoModel)
async def obtener_movimiento(
    mov_id: str,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token),
):
    return movimiento_controller.obtener_movimiento(db, user.user_id, mov_id)

# Crear nuevos movimientos de una cuenta
@router.post("/", response_model=NuevoMovimientoResponse)
async def crear_movimiento(
    request: CreateNewMovimiento,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token)
):
    
    return movimiento_controller.crear_movimiento(db, user.user_id, request)

# Crear metodo para actualizar los movimientos
@router.patch("/{id}")
async def actualizar_movimiento(
    id:str,
    new_movimiento: ActualizarMovimiento,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token)
):
    return movimiento_controller.actualizar_movimiento(db, user.user_id, id, new_movimiento)

# Crear metodo para eliminar los movimientos
@router.delete("/{id}")
async def eliminar_movimiento(
    id: str,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token)
):
    return movimiento_controller.eliminar_movimiento(db, user.user_id, id)
    

