from fastapi import APIRouter, Depends, Query, Request
from typing import List, Optional

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from schemas.movimientos_schema import (
    CreateNewMovimiento,
    NuevoMovimientoResponse,
    ObtenerMovimientos
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
    orden: str = "desc"
):
    base_url = str(request.url.replace(query=None))
    return movimiento_controller.obtener_movimientos(db, user.user_id, limit, offset, orden, base_url)

# Crear nuevos movimientos de una cuenta
@router.post("/", response_model=NuevoMovimientoResponse)
async def crear_movimiento(
    request: CreateNewMovimiento,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token)
):
    
    return movimiento_controller.crear_movimiento(db, user.user_id, request)

@router.get("/{id}")
async def obtener_movimiento():
    pass

@router.put("/{id}")
async def actualizar_movimiento():
    pass

@router.delete("/{id}")
async def eliminar_movimiento():
    pass

