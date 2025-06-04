from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

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