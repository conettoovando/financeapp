from fastapi import Request, HTTPException
from sqlalchemy.orm import Session, joinedload
from models.cuenta import TipoCuenta
from models.banco import Banco
from sqlalchemy import select
from schemas.formularios_schema import CreateCuentaResponse

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