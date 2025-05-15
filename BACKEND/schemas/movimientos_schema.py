from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional
from datetime import datetime

from models.cuenta import Cuenta
from models.movimiento import Movimiento

class CreateNewMovimiento(BaseModel):
    cuenta_id: str
    movimiento_id: str
    monto: int
    fecha: datetime
    categoria_id: str
    destinatario_id: Optional[str] = None

class CuentaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    saldo: int

class TipoMovimientoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tipo: str

class CategoriaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nombre: str

class NuevoMovimientoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nuevo_saldo: int
    tipo: str
    monto: int
    fecha: datetime
    categoria: str
    destinatario: Optional[CategoriaResponse]

    @classmethod
    def from_orm_full(cls, movimiento: Movimiento):
        return cls(
            id=movimiento.id,
            nuevo_saldo=movimiento.cuenta.saldo,
            tipo=movimiento.tipo_movimiento.tipo,
            monto=movimiento.monto,
            fecha=movimiento.fecha,
            categoria=movimiento.categoria.nombre,
            destinatario=CategoriaResponse.model_validate(movimiento.destinatario) if movimiento.destinatario else None
        )