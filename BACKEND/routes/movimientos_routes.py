from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from schemas.movimientos_schema import (
    CreateNewMovimiento,
    NuevoMovimientoResponse
)
from schemas.user_schema import VerifyToken
from database.finance import get_db
from controllers import movimiento_controller
from controllers import user_controller

router = APIRouter()

# Crear nuevos movimientos de una cuenta
@router.post("/", response_model=NuevoMovimientoResponse)
async def crear_movimiento(
    request: CreateNewMovimiento,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token)
):
    return movimiento_controller.crear_movimiento(db, user, request)
