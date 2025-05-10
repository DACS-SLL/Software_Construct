from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Evaluacion(Base):
    __tablename__ = "evaluacion"
    id = Column(Integer, primary_key=True, index=True)
    postulacion_id = Column(Integer, ForeignKey("postulacion.id"))
    evaluador_id = Column(Integer, ForeignKey("usuario.id"))
    comentario = Column(Text)
    puntaje = Column(Integer)

    postulacion = relationship("Postulacion")
    evaluador = relationship("Usuario")