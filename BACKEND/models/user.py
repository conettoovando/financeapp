from sqlalchemy import Column, String, DateTime, TIMESTAMP, func, text
from database.user import Base
import uuid
from sqlalchemy.dialects.mysql import BINARY as MYSQL_BINARY

class Users(Base):
    __tablename__ = "Users"

    id = Column(MYSQL_BINARY(16), primary_key=True, index=True, server_default=text("UUID_TO_BIN(UUID())"))
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

