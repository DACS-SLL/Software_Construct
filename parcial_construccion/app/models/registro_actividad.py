from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class RegistroActividad(Base):
    __tablename__ = "registro_actividad"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    accion = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")