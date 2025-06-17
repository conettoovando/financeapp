from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from schemas.categoria_schema import (
    CategoriasResponse,
    CreateCategoryModel
)
from schemas.user_schema import VerifyToken
from controllers import categorias_controller
from database.finance import get_db
from controllers import user_controller

router = APIRouter()

@router.get("/", response_model=list[CategoriasResponse])
def obtener_categorias(
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token)
):
    return categorias_controller.obtener_categorias(db, user.user_id)
    
@router.post("/")
def crear_categoria(
    body: CreateCategoryModel,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token)
):
    return categorias_controller.crear_categoria(db, user.user_id, body)

@router.put("/{id}")
def actualizar_categoria(
    body: CreateCategoryModel,
    id: str,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token)
):
    return categorias_controller.actualizar_categoria(db, user.user_id, body, id)

@router.delete("/{id}")
def eliminar_categoria(
    id: str,
    db: Session = Depends(get_db),
    user: VerifyToken = Depends(user_controller.verify_token)
):
    return categorias_controller.eliminar_categoria(db, user.user_id, id)