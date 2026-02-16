import enum
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Enum, text
from app.db.base import Base

class RoleEnum(str, enum.Enum):
    USER = "user"
    MODEL = "model"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    role = Column(Enum(RoleEnum, values_callable=lambda x: [e.value for e in x]), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('now()'))
