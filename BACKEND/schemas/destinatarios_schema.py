from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateDestModel(BaseModel):
    nombre: str