from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional
from datetime import datetime

class CreateCategoryModel(BaseModel):
    nombre: str