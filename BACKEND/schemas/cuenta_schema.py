from pydantic import BaseModel, HttpUrl, ConfigDict
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

class DeleteCuentaRequest(BaseModel):
    cuenta_id: str

class GetTipoCuentaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tipo: str

class GetBancoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nombre_banco: str
    url: HttpUrl

class GetCuetasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    nombre_cuenta: str | None = None
    saldo: int | None = None
    limite_credito: int | None = None
    fecha_facturacion: datetime | None = None
    fecha_pago: datetime | None = None
    tipo_cuenta: GetTipoCuentaResponse
    banco: GetBancoResponse



    