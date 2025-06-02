from sqlalchemy import Column, String, CHAR, ForeignKey, text
from sqlalchemy.orm import relationship
from database.finance import Base

class Destinatario(Base):
    __tablename__ = "Destinatario"

    id = Column(CHAR(36), primary_key=True, server_default=text("gen_random_uuid()"))
    usuario_id = Column(CHAR(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(50), nullable=False)

    usuario = relationship("Users", back_populates="destinatarios")
