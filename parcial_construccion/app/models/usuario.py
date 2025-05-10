# app/models/usuario.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Rol(Base):
    __tablename__ = "rol"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True, nullable=False)
    contraseña_hash = Column(String)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)
    rol_id = Column(Integer, ForeignKey("rol.id"))

    rol = relationship("Rol")
