from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)