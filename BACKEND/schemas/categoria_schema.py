from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional
from datetime import datetime

class CreateCategoryModel(BaseModel):
    nombre: str

class CategoriasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre: str
    usuario_id: str | None
    