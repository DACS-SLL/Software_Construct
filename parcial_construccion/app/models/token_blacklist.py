from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    fecha_revocado = Column(DateTime, default=datetime.utcnow)
