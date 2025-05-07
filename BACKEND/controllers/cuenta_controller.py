import requests
import jwt
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from models.banco import Banco
from models.cuenta import TipoCuenta, Cuenta
from models.user import Users
from schemas.cuenta_schema import CreateCuentaRequest, UpdateCuentaRequest, VerifyToken
from sqlalchemy import select

AUTH_PUBLIC_KEY_URL = "http://localhost:8000/auth/public-key"
ALGORITHM="RS256"

def get_public_key():
    res = requests.get(AUTH_PUBLIC_KEY_URL)
    if res.status_code != 200:
        raise RuntimeError("No se pudo obtener la clave pública")
    return res.text

def authorization_error():
    return HTTPException(status_code=400, detail="Usuario no autorizado")

public_key = get_public_key()

def verify_token(request: Request) -> VerifyToken:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    try:
        payload = jwt.decode(token, public_key, algorithms=ALGORITHM)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token sin 'sub'")
        
        return VerifyToken(
            user_id=user_id
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")
    
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

    
    if cuenta.user_id != user_id:
        raise authorization_error()
    
    # Actualizar los campos de la cuenta
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cuenta, key, value)

    db.commit()
    db.refresh(cuenta)
    
    return cuenta