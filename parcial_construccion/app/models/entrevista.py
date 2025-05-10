from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Entrevista(Base):
    __tablename__ = "entrevista"
    id = Column(Integer, primary_key=True, index=True)
    postulacion_id = Column(Integer, ForeignKey("postulacion.id"))
    fecha = Column(DateTime)
    modalidad = Column(String)
    resultado = Column(String)

    postulacion = relationship("Postulacion")

    
