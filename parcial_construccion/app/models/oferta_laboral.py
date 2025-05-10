from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class OfertaLaboral(Base):
    __tablename__ = "oferta_laboral"
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"))
    titulo = Column(String)
    descripcion = Column(Text)
    ubicacion = Column(String)
    fecha_publicacion = Column(Date)
    categoria_id = Column(Integer, ForeignKey("categoria.id"))
    estado = Column(String)

    empresa = relationship("Empresa")
    categoria = relationship("Categoria")