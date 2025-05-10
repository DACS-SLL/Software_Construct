from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Notificacion(Base):
    __tablename__ = "notificacion"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    mensaje = Column(Text)
    leida = Column(Boolean, default=False)
    fecha_envio = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")