from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Curriculum(Base):
    __tablename__ = "curriculum"
    id = Column(Integer, primary_key=True, index=True)
    postulante_id = Column(Integer, ForeignKey("postulante.id"))
    ruta_archivo = Column(String)
    fecha_subida = Column(DateTime, default=datetime.utcnow)

    postulante = relationship("Postulante")