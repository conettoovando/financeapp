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