from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class ExperienciaLaboral(Base):
    __tablename__ = "experiencia_laboral"
    id = Column(Integer, primary_key=True, index=True)
    curriculum_id = Column(Integer, ForeignKey("curriculum.id"))
    empresa = Column(String)
    cargo = Column(String)
    descripcion = Column(Text)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)

    curriculum = relationship("Curriculum")