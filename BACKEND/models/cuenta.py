from sqlalchemy import Column, String, Integer, CHAR, DateTime, ForeignKey, func, text
from sqlalchemy.orm import relationship
from database.finance import Base

class Cuenta(Base):
    __tablename__ = "Cuenta"

    id = Column(CHAR(36), primary_key=True, server_default=text("uuid_generate_v4()"))
    nombre_cuenta = Column(String(30))
    tipo_cuenta_id = Column(CHAR(36), ForeignKey("TipoCuenta.id", ondelete="RESTRICT"), nullable=False)
    saldo = Column(Integer, default=0)
    banco_id = Column(CHAR(36), ForeignKey("Banco.id", ondelete="CASCADE"), nullable=False)
    limite_credito = Column(Integer, nullable=True)
    fecha_facturacion = Column(DateTime, nullable=True)
    fecha_pago = Column(DateTime, nullable=True)
    user_id = Column(CHAR(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    usuario = relationship("Users", back_populates="cuentas")
    banco = relationship("Banco", back_populates="cuentas")
    tipo_cuenta = relationship("TipoCuenta", back_populates="cuentas")
    movimientos = relationship("Movimiento", back_populates="cuenta", cascade="all, delete")

class TipoCuenta(Base):
    __tablename__ = "TipoCuenta"

    id = Column(CHAR(36), primary_key=True, server_default=text("uuid_generate_v4()"))
    tipo = Column(String(30), nullable=False)

    cuentas = relationship("Cuenta", back_populates="tipo_cuenta")