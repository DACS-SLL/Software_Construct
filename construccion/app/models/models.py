from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Rol(Base):
    __tablename__ = "rol"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True, nullable=False)
    contraseña_hash = Column(String)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)
    rol_id = Column(Integer, ForeignKey("rol.id"))

    rol = relationship("Rol")

class Empresa(Base):
    __tablename__ = "empresa"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    nombre = Column(String)
    rubro = Column(String)
    direccion = Column(String)
    descripcion = Column(Text)

    usuario = relationship("Usuario")

class Postulante(Base):
    __tablename__ = "postulante"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    nombre_completo = Column(String)
    fecha_nacimiento = Column(Date)
    telefono = Column(String)

    usuario = relationship("Usuario")

class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

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


class Postulacion(Base):
    __tablename__ = "postulacion"
    id = Column(Integer, primary_key=True, index=True)
    postulante_id = Column(Integer, ForeignKey("postulante.id"))
    oferta_id = Column(Integer, ForeignKey("oferta_laboral.id"))
    fecha_postulacion = Column(Date)
    estado = Column(String)

    postulante = relationship("Postulante")
    oferta = relationship("OfertaLaboral")


class Curriculum(Base):
    __tablename__ = "curriculum"
    id = Column(Integer, primary_key=True, index=True)
    postulante_id = Column(Integer, ForeignKey("postulante.id"))
    ruta_archivo = Column(String)
    fecha_subida = Column(DateTime, default=datetime.utcnow)

    postulante = relationship("Postulante")


class Educacion(Base):
    __tablename__ = "educacion"
    id = Column(Integer, primary_key=True, index=True)
    curriculum_id = Column(Integer, ForeignKey("curriculum.id"))
    institucion = Column(String)
    titulo = Column(String)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)

    curriculum = relationship("Curriculum")


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


class Entrevista(Base):
    __tablename__ = "entrevista"
    id = Column(Integer, primary_key=True, index=True)
    postulacion_id = Column(Integer, ForeignKey("postulacion.id"))
    fecha = Column(DateTime)
    modalidad = Column(String)
    resultado = Column(String)

    postulacion = relationship("Postulacion")


class Habilidad(Base):
    __tablename__ = "habilidad"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)


class Notificacion(Base):
    __tablename__ = "notificacion"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    mensaje = Column(Text)
    leida = Column(Boolean, default=False)
    fecha_envio = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")


class Mensaje(Base):
    __tablename__ = "mensaje"
    id = Column(Integer, primary_key=True, index=True)
    emisor_id = Column(Integer, ForeignKey("usuario.id"))
    receptor_id = Column(Integer, ForeignKey("usuario.id"))
    contenido = Column(Text)
    fecha_envio = Column(DateTime, default=datetime.utcnow)

    emisor = relationship("Usuario", foreign_keys=[emisor_id])
    receptor = relationship("Usuario", foreign_keys=[receptor_id])


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    fecha_revocado = Column(DateTime, default=datetime.utcnow)


class Evaluacion(Base):
    __tablename__ = "evaluacion"
    id = Column(Integer, primary_key=True, index=True)
    postulacion_id = Column(Integer, ForeignKey("postulacion.id"))
    evaluador_id = Column(Integer, ForeignKey("usuario.id"))
    comentario = Column(Text)
    puntaje = Column(Integer)

    postulacion = relationship("Postulacion")
    evaluador = relationship("Usuario")


class RegistroActividad(Base):
    __tablename__ = "registro_actividad"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    accion = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")
