from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from schemas.categoria_schema import CategoriasResponse
from schemas.cuenta_schema import GetCuetasResponse
from schemas.movimientos_schema import TipoMovimientoResponse

class Banco(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    nombre_banco: str
    url: str | None

class TipoCuenta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tipo: str

class CreateCuentaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tipo_cuenta: list[TipoCuenta]
    banco: list[Banco]

class Cuenta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre_cuenta: str

class CreateMovimientoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cuentas: list[Cuenta]
    tipo_movimientos: list[TipoMovimientoResponse]
    categorias: list[CategoriasResponse]