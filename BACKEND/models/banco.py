from sqlalchemy import Column, String, CHAR, text
from sqlalchemy.orm import relationship
from database.finance import Base

class Banco(Base):
    __tablename__ = "Banco"

    id = Column(CHAR(36), primary_key=True, server_default=text("uuid_generate_v4()"))
    nombre_banco = Column(String(100), nullable=False)
    url = Column(String(150))

    cuentas = relationship("Cuenta", back_populates="banco", cascade="all, delete")
