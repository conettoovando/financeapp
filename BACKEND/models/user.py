from sqlalchemy import Column, String, Integer, CHAR, DateTime, ForeignKey, TIMESTAMP, func, text
from sqlalchemy.orm import relationship
from database.user import Base

class Users(Base):
    __tablename__ = "Users"

    id = Column(CHAR(36), primary_key=True, index=True, server_default=text("UUID()"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    destinatarios = relationship("Destinatario", back_populates="usuario", cascade="all, delete")
    cuentas = relationship("Cuenta", back_populates="usuario", cascade="all, delete")
    movimientos = relationship("Movimiento", back_populates="usuario", cascade="all, delete")

class Destinatario(Base):
    __tablename__ = "Destinatario"

    id = Column(CHAR(36), primary_key=True, server_default=("UUID()"))
    usuario_id = Column(CHAR(36), ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(50), nullable=False)

    usuario = relationship("Users", back_populates="destinatarios")

class Banco(Base):
    __tablename__ = "Banco"

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
    nombre_banco = Column(String(30), nullable=False)
    url = Column(String(90))

    cuentas = relationship("Cuenta", back_populates="banco", cascade="all, delete")

class TipoCuenta(Base):
    __tablename__ = "TipoCuenta"

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
    tipo = Column(String(30), nullable=False)

    cuentas = relationship("Cuenta", back_populates="tipo_cuenta")

class Cuenta(Base):
    __tablename__ = "Cuenta"

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
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

class TipoMovimiento(Base):
    __tablename__ = "TipoMovimiento"

    id = Column(CHAR(36), primary_key=True, server_default=("UUID()"))
    tipo = Column(String(30), nullable=False)

    movimientos = relationship("Movimiento", back_populates="tipo_movimiento")

class Categoria(Base):
    __tablename__ = "Categoria"

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
    nombre = Column(String(30), nullable=False)

    movimientos = relationship("Movimiento", back_populates="categoria")

class Movimiento(Base):
    __tablename__ = "Movimiento"

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
    cuenta_id = Column(CHAR(36), ForeignKey("Cuenta.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(CHAR(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    TipoMovimiento_id = Column(CHAR(36), ForeignKey("TipoMovimiento.id", ondelete="RESTRICT"), nullable=False)
    monto = Column(Integer, nullable=False, default=0)
    fecha = Column(DateTime, server_default=func.now())
    categoria_id = Column(CHAR(36), ForeignKey("Categoria.id", ondelete="RESTRICT"), nullable=False)
    destinatario_id = Column(CHAR(36), ForeignKey("Destinatario.id", ondelete="SET NULL"), nullable=True)

    usuario = relationship("Cuenta", back_populates="movimientos")
    cuenta = relationship("Cuenta", back_populates="movimientos")
    tipo_movimiento = relationship("TipoMovimiento", back_populates="movimientos")
    categoria = relationship("Categoria", back_populates="movimientos")
    destinatario = relationship("Destinatario")