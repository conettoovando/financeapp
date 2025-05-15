from fastapi import HTTPException
# SQLALCHEMY
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
# Modelos
from models.cuenta import TipoCuenta, Cuenta
from models.movimiento import Movimiento, TipoMovimiento
from models.categoria import Categoria
#SCHEMAS
from schemas.movimientos_schema import CreateNewMovimiento, NuevoMovimientoResponse
# UTILS
from datetime import datetime, timezone

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
            (Cuenta.id == request.cuenta_id) & (Cuenta.user_id == user.user_id),
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
            usuario_id=user.user_id,
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
