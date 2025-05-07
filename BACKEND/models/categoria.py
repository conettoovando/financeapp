from sqlalchemy import Column, String, CHAR, text
from sqlalchemy.orm import relationship
from database.finance import Base

class Categoria(Base):
    __tablename__ = "Categoria"

    id = Column(CHAR(36), primary_key=True, server_default=text("uuid_generate_v4()"))
    nombre = Column(String(30), nullable=False)

    movimientos = relationship("Movimiento", back_populates="categoria")

