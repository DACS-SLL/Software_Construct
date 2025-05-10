from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Postulante(Base):
    __tablename__ = "postulante"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    nombre_completo = Column(String)
    fecha_nacimiento = Column(Date)
    telefono = Column(String)

    usuario = relationship("Usuario")
    curriculum = relationship("Curriculum", back_populates="postulante")
