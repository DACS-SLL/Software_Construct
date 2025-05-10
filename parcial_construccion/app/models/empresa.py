from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Empresa(Base):
    __tablename__ = "empresa"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    nombre = Column(String)
    rubro = Column(String)
    direccion = Column(String)
    descripcion = Column(Text)

    usuario = relationship("Usuario")
