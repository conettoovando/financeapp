from typing import Optional
from fastapi import HTTPException
# SQLALCHEMY
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
# Modelos
from models.cuenta import TipoCuenta, Cuenta
from models.movimiento import Movimiento, TipoMovimiento
from models.categoria import Categoria
#SCHEMAS
from schemas.movimientos_schema import (
    CreateNewMovimiento,
    MovimientoModel,
    NuevoMovimientoResponse,
    ActualizarMovimiento
)
# UTILS
from datetime import datetime, timezone
from urllib.parse import urlencode

def obtener_o_404(db: Session, modelo, filtro, mensaje_error: str):
    instancia = db.execute(select(modelo).filter(filtro)).scalar_one_or_none()
    if not instancia:
        raise HTTPException(status_code=400, detail=mensaje_error)
    return instancia

def crear_movimiento(db: Session, user: str, request: CreateNewMovimiento):
    try:
        cuenta = obtener_o_404(
            db,
            Cuenta,
            (Cuenta.id == request.cuenta_id) & (Cuenta.user_id == user),
            "Cuenta o usuario no registrado"
        )

        tipo_mov = obtener_o_404(
            db,
            TipoMovimiento,
            TipoMovimiento.id == request.movimiento_id,
            "Movimiento no registrado"
        )

        obtener_o_404(
            db,
            Categoria,
            Categoria.id == request.categoria_id,
            "Categoría no registrada"
        )

        nuevo_movimiento = Movimiento(
            cuenta_id=request.cuenta_id,
            usuario_id=user,
            TipoMovimiento_id=request.movimiento_id,
            monto=request.monto,
            fecha=request.fecha or datetime.now(timezone.utc),
            categoria_id=request.categoria_id,
            destinatario_id=request.destinatario_id
        )

        db.add(nuevo_movimiento)

        if tipo_mov.tipo == "Gasto":
            cuenta.saldo -= request.monto
        elif tipo_mov.tipo == "Ingreso":
            cuenta.saldo += request.monto

        db.commit()

        movimiento = db.execute(
            select(Movimiento)
            .options(
                joinedload(Movimiento.cuenta),
                joinedload(Movimiento.tipo_movimiento),
                joinedload(Movimiento.categoria),
                joinedload(Movimiento.destinatario)
            )
            .filter(Movimiento.id == nuevo_movimiento.id)
        ).scalar_one()

        return NuevoMovimientoResponse.from_orm_full(movimiento)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el movimiento: {str(e)}")

from fastapi import HTTPException, status

def obtener_movimientos(
    db: Session,
    user: str,
    limit: int,
    offset: int,
    orden: str,
    base_url: str,
    cuenta_id: Optional[str] = None
):
    print(f"Movimiento de la cuenta {cuenta_id}")
    query = select(Movimiento).filter(Movimiento.usuario_id == user)

    if cuenta_id is not None:
        # 🛡️ Verificar que la cuenta pertenezca al usuario
        cuenta = db.execute(
            select(Cuenta).filter(Cuenta.id == cuenta_id, Cuenta.user_id == user)
        ).scalar_one_or_none()

        if cuenta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La cuenta no existe o no pertenece al usuario"
            )

        query = query.filter(Movimiento.cuenta_id == cuenta_id)

    total = db.execute(
        select(func.count()).select_from(query.subquery())
    ).scalar()

    orden_columna = Movimiento.fecha.desc() if orden == "desc" else Movimiento.fecha.asc()

    movimientos = db.execute(
        query
        .order_by(orden_columna)
        .limit(limit)
        .offset(offset)
        .options(
            joinedload(Movimiento.cuenta),
            joinedload(Movimiento.tipo_movimiento),
            joinedload(Movimiento.categoria),
            joinedload(Movimiento.destinatario),
        )
    ).scalars().all()

    next_offset = offset + limit
    prev_offset = offset - limit if offset - limit >= 0 else None

    query_params = {"offset": offset, "limit": limit, "orden": orden}
    if cuenta_id is not None:
        query_params["cuenta_id"] = cuenta_id

    next_url = (
        f"{base_url}?{urlencode({**query_params, 'offset': next_offset})}"
        if total and next_offset < total else None
    )

    prev_url = (
        f"{base_url}?{urlencode({**query_params, 'offset': prev_offset})}"
        if prev_offset is not None else None
    )

    return {
        "count": total,
        "next": next_url,
        "previous": prev_url,
        "results": [MovimientoModel.from_orm_full(m) for m in movimientos],
    }



def obtener_movimiento(db: Session, user_id: str, mov_id):
    movimiento = db.execute(
        select(Movimiento)
        .filter((Movimiento.id == mov_id) & (Movimiento.usuario_id == user_id))
        .options(
            joinedload(Movimiento.categoria),
            joinedload(Movimiento.tipo_movimiento),
            joinedload(Movimiento.destinatario),
            joinedload(Movimiento.cuenta)
        )
    ).scalar_one_or_none()

    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no registrado")
    
    return MovimientoModel.from_orm_full(movimiento)

def actualizar_movimiento(db: Session, user_id: str, mov_id: str, new_movimiento: ActualizarMovimiento):
    movimiento = db.get(Movimiento, mov_id)
    if movimiento is None or str(movimiento.usuario_id) != str(user_id):
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    
    for campo, valor in new_movimiento.model_dump(exclude_unset=True).items():
        setattr(movimiento, campo, valor)

    db.commit()
    db.refresh(movimiento)

    return movimiento

def eliminar_movimiento(db: Session, user_id: str, mov_id: str):
    movimiento = db.get(Movimiento, mov_id)

    if movimiento is None or str(movimiento.usuario_id) != user_id:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    db.delete(movimiento)
    db.commit()

    return {"message": "Movimiento eliminado correctamente"}


