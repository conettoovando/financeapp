from sqlalchemy import Column, String, CHAR, text, ForeignKey
from sqlalchemy.orm import relationship
from database.finance import Base

class Categoria(Base):
    __tablename__ = "Categoria"

    id = Column(CHAR(36), primary_key=True, server_default=text("gen_random_uuid()"))
    nombre = Column(String(30), nullable=False)
    usuario_id = Column(CHAR(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=True)

    usuario = relationship("Users", back_populates="categorias")
    movimientos = relationship("Movimiento", back_populates="categoria")

