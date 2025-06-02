from sqlalchemy import Column, CHAR, DateTime, TIMESTAMP, func, text
from sqlalchemy.orm import relationship
from database.finance import Base

class Users(Base):
    __tablename__ = "Users"

    id = Column(CHAR(36), primary_key=True, index=True, server_default=text("gen_random_uuid()"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    destinatarios = relationship("Destinatario", back_populates="usuario", cascade="all, delete")
    cuentas = relationship("Cuenta", back_populates="usuario", cascade="all, delete")
    movimientos = relationship("Movimiento", back_populates="usuario", cascade="all, delete")
    categorias = relationship("Categoria", back_populates="usuario", cascade="all, delete")