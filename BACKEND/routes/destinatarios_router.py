from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from schemas.destinatarios_schema import (
    CreateDestModel
)
from schemas.user_schema import VerifyToken
from controllers import destinatarios_controller
from controllers.user_controller import verify_token
from database.finance import get_db

router = APIRouter()

@router.get("/")
async def obtener_destinatarios(
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(verify_token)
):
    return destinatarios_controller.obtener_destinataios(
        db,
        user.user_id
    )

@router.post("/")
async def crear_destinatario(
    body: CreateDestModel, 
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(verify_token)
):
    return destinatarios_controller.crear_destinatario(
        db,
        user.user_id,
        body
    )

@router.patch("/{dest_id}")
async def actualizar_destinatario(
    body: CreateDestModel,
    dest_id: str,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(verify_token)
):
    return destinatarios_controller.actualizar_destinatario(
        db, user.user_id, dest_id, body
    )

@router.delete("/{dest_id}")
async def eliminar_destinatario(
    dest_id: str,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(verify_token)
):
    return destinatarios_controller.eliminar_destinatario(
        db, user.user_id, dest_id
    )