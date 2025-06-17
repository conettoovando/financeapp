from fastapi import Request, HTTPException
from sqlalchemy.orm import Session, joinedload
from models.categoria import Categoria
from models.cuenta import Cuenta, TipoCuenta
from models.banco import Banco
from sqlalchemy import select
from models.movimiento import TipoMovimiento
from schemas.formularios_schema import CreateCuentaResponse, CreateMovimientoResponse

def crearCuenta(
        db: Session,
        user: str
):
    """
    tipo_cuenta
    banco
    """

    tipo_cuenta_models = list(db.execute(select(TipoCuenta)).scalars().all())
    banco_models = list(db.execute(select(Banco)).scalars().all())

    tipo_cuenta = [CreateCuentaResponse.__annotations__['tipo_cuenta'].__args__[0].from_orm(tc) for tc in tipo_cuenta_models]
    banco = [CreateCuentaResponse.__annotations__['banco'].__args__[0].from_orm(b) for b in banco_models]

    return CreateCuentaResponse(
        tipo_cuenta=tipo_cuenta,
        banco=banco
    )

def crearMovimiento(
        db: Session,
        user: str
):
    cuentas = list(db.execute(select(Cuenta)).scalars().all())
    tipo_movimientos = list(db.execute(
        select(TipoMovimiento)
    ).scalars().all())
    categorias = list(db.execute(
        select(Categoria)
        .where((Categoria.usuario_id == user or Categoria.usuario_id == None))
    ).scalars().all())

    cuentas_schema = [CreateMovimientoResponse.__annotations__['cuentas'].__args__[0].from_orm(c) for c in cuentas]
    tipo_movimiento_schema = [CreateMovimientoResponse.__annotations__['tipo_movimientos'].__args__[0].from_orm(c) for c in tipo_movimientos]
    categorias_schema = [CreateMovimientoResponse.__annotations__['categorias'].__args__[0].from_orm(c) for c in categorias]

    return CreateMovimientoResponse(
        cuentas=cuentas_schema,
        tipo_movimientos=tipo_movimiento_schema,
        categorias=categorias_schema
    )