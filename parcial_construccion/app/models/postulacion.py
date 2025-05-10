from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Postulacion(Base):
    __tablename__ = "postulacion"
    id = Column(Integer, primary_key=True, index=True)
    postulante_id = Column(Integer, ForeignKey("postulante.id"))
    oferta_id = Column(Integer, ForeignKey("oferta_laboral.id"))
    fecha_postulacion = Column(Date)
    estado = Column(String)

    postulante = relationship("Postulante")
    oferta = relationship("OfertaLaboral")