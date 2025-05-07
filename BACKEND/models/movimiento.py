from sqlalchemy import Column, String, Integer, CHAR, DateTime, ForeignKey, func, text
from sqlalchemy.orm import relationship
from database.finance import Base


class Movimiento(Base):
    __tablename__ = "Movimiento"

    id = Column(CHAR(36), primary_key=True, server_default=text("uuid_generate_v4()"))
    cuenta_id = Column(CHAR(36), ForeignKey("Cuenta.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(CHAR(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    TipoMovimiento_id = Column(CHAR(36), ForeignKey("TipoMovimiento.id", ondelete="RESTRICT"), nullable=False)
    monto = Column(Integer, nullable=False, default=0)
    fecha = Column(DateTime, server_default=func.now())
    categoria_id = Column(CHAR(36), ForeignKey("Categoria.id", ondelete="RESTRICT"), nullable=False)
    destinatario_id = Column(CHAR(36), ForeignKey("Destinatario.id", ondelete="SET NULL"), nullable=True)

    usuario = relationship("Users", back_populates="movimientos")
    cuenta = relationship("Cuenta", back_populates="movimientos")
    tipo_movimiento = relationship("TipoMovimiento", back_populates="movimientos")
    categoria = relationship("Categoria", back_populates="movimientos")
    destinatario = relationship("Destinatario")

class TipoMovimiento(Base):
    __tablename__ = "TipoMovimiento"

    id = Column(CHAR(36), primary_key=True, server_default=("uuid_generate_v4()"))
    tipo = Column(String(30), nullable=False)

    movimientos = relationship("Movimiento", back_populates="tipo_movimiento")
