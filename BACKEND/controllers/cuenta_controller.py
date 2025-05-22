import requests
import jwt
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session, joinedload
from models.banco import Banco
from models.cuenta import TipoCuenta, Cuenta
from models.user import Users
from schemas.cuenta_schema import CreateCuentaRequest, UpdateCuentaRequest, DeleteCuentaRequest
from sqlalchemy import select

def authorization_error():
    return HTTPException(status_code=400, detail="Usuario no autorizado")

def obtener_cuentas(db: Session, user: str):
    cuentas = db.execute(
        select(Cuenta)
        .options(joinedload(Cuenta.banco), joinedload(Cuenta.tipo_cuenta))
        .filter(Cuenta.user_id == user)
    ).scalars().all()

    return cuentas

def obtener_cuenta(db: Session, user: str, account_id: str):
    print(f"Toca retornar solo el elemento del id {account_id}")
    cuenta = db.execute(
        select(Cuenta)
        .options(joinedload(Cuenta.banco), joinedload(Cuenta.tipo_cuenta))
        .filter(
            Cuenta.user_id == user,
            Cuenta.id == account_id
        )
    ).scalar_one_or_none()

    return cuenta

def crear_cuenta(request: CreateCuentaRequest, db: Session):
    # Validar tipo de cuenta
    tipo_cuenta = db.execute(select(TipoCuenta).filter(TipoCuenta.id == request.tipo_cuenta_id)).scalar_one_or_none()
    if not tipo_cuenta:
        raise HTTPException(status_code=400, detail="Tipo de cuenta no valido")
    
    # Validar banco
    banco = db.execute(select(Banco).filter(Banco.id == request.banco_id)).scalar_one_or_none()
    if not banco:
        raise HTTPException(status_code=400, detail="Banco no valido")

    usuario = db.execute(select(Users).filter(Users.id == request.user_id)).scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    cuenta = Cuenta(
        nombre_cuenta=request.nombre_cuenta,
        tipo_cuenta=tipo_cuenta,
        banco=banco,
        usuario=usuario,
        saldo=request.saldo,
        limite_credito=request.limite_credito,
        fecha_facturacion=request.fecha_facturacion,
        fecha_pago=request.fecha_pago        
    )

    db.add(cuenta)
    db.commit()
    db.refresh(cuenta)

    return cuenta

def actualizar_cuenta(request: UpdateCuentaRequest, db: Session, user_id: str):
    cuenta = db.execute(select(Cuenta).filter(Cuenta.id == request.id)).scalar_one_or_none()

    if not cuenta:
        raise HTTPException(status_code=400, detail="Cuenta no encontrada")

    
    if str(cuenta.user_id) != user_id:
        raise authorization_error()
    
    # Actualizar los campos de la cuenta
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cuenta, key, value)

    db.commit()
    db.refresh(cuenta)
    
    return cuenta

def eliminar_cuenta(request: DeleteCuentaRequest, db: Session, user_id):
    cuenta = db.execute(select(Cuenta).filter(Cuenta.id == request.cuenta_id)).scalar_one_or_none()

    if not cuenta:
        raise HTTPException(status_code=400, detail="Cuenta no encontrada")
    
    if cuenta.user_id != user_id:
        raise authorization_error()
    
    db.delete(cuenta)
    db.commit()

    return {"msg": "Cuenta eliminada con exito"}