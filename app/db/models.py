from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Enum, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class RoleEnum(str, enum.Enum):
    user = "user"
    model = "model"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    role = Column(Enum(RoleEnum), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
