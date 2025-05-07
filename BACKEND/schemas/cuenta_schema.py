from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateCuentaRequest(BaseModel):
    nombre_cuenta: str
    tipo_cuenta_id: str
    banco_id: str
    user_id: str
    saldo: int
    limite_credito: Optional[int] = None
    fecha_facturacion: Optional[datetime] = None
    fecha_pago: Optional[datetime] = None

class UpdateCuentaRequest(BaseModel):
    id: str
    nombre_cuenta:Optional[str] = None
    tipo_cuenta_id: Optional[str] = None
    banco_id: Optional[str] = None
    user_id: Optional[str] = None
    saldo: Optional[int] = None
    limite_credito: Optional[int] = None
    fecha_facturacion: Optional[datetime] = None
    fecha_pago: Optional[datetime] = None

class VerifyToken(BaseModel):
    user_id: str