from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware  # ← AGREGAR ESTA LÍNEA
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.database import Base, engine
import uvicorn

from app.database import SessionLocal, engine
from app.models import models
from pydantic import BaseModel, Field
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plataforma de Empleo API",
    description="API para la gestión de ofertas y solicitudes de empleo",
    version="1.0.0"
)

# ← AGREGAR ESTAS LÍNEAS DESPUÉS DE CREAR LA APP:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],   # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],   # Permite todos los headers
)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request/response
# -------------------------------------

# Usuario schemas
class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):
    pass

class Rol(RolBase):
    id: int

    class Config:
        orm_mode = True

class UsuarioBase(BaseModel):
    nombre: Optional[str] = None
    email: str
    activo: Optional[bool] = True
    rol_id: int

class UsuarioCreate(UsuarioBase):
    contraseña: str

class Usuario(UsuarioBase):
    id: int
    fecha_registro: datetime

    class Config:
        orm_mode = True

# Empresa schemas
class EmpresaBase(BaseModel):
    nombre: str
    rubro: Optional[str] = None
    direccion: Optional[str] = None
    descripcion: Optional[str] = None
    usuario_id: Optional[int] = None

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int

    class Config:
        orm_mode = True

# Postulante schemas
class PostulanteBase(BaseModel):
    nombre_completo: str
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[str] = None
    usuario_id: Optional[int] = None

class PostulanteCreate(PostulanteBase):
    pass

class Postulante(PostulanteBase):
    id: int

    class Config:
        orm_mode = True

# Categoría schemas
class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        orm_mode = True

# Oferta Laboral schemas
class OfertaLaboralBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    categoria_id: int
    empresa_id: int
    estado: str = "activa"

class OfertaLaboralCreate(OfertaLaboralBase):
    pass

class OfertaLaboral(OfertaLaboralBase):
    id: int

    class Config:
        orm_mode = True

# Postulación schemas
class PostulacionBase(BaseModel):
    postulante_id: int
    oferta_id: int
    fecha_postulacion: Optional[date] = None
    estado: str = "pendiente"

class PostulacionCreate(PostulacionBase):
    pass

class Postulacion(PostulacionBase):
    id: int

    class Config:
        orm_mode = True

# Curriculum schemas
class CurriculumBase(BaseModel):
    postulante_id: int
    ruta_archivo: str

class CurriculumCreate(CurriculumBase):
    pass

class Curriculum(CurriculumBase):
    id: int
    fecha_subida: datetime

    class Config:
        orm_mode = True

# Educación schemas
class EducacionBase(BaseModel):
    curriculum_id: int
    institucion: str
    titulo: str
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class EducacionCreate(EducacionBase):
    pass

class Educacion(EducacionBase):
    id: int

    class Config:
        orm_mode = True

# Experiencia Laboral schemas
class ExperienciaLaboralBase(BaseModel):
    curriculum_id: int
    empresa: str
    cargo: str
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class ExperienciaLaboralCreate(ExperienciaLaboralBase):
    pass

class ExperienciaLaboral(ExperienciaLaboralBase):
    id: int

    class Config:
        orm_mode = True

# Entrevista schemas
class EntrevistaBase(BaseModel):
    postulacion_id: int
    fecha: datetime
    modalidad: str
    resultado: Optional[str] = None

class EntrevistaCreate(EntrevistaBase):
    pass

class Entrevista(EntrevistaBase):
    id: int

    class Config:
        orm_mode = True

# Habilidad schemas
class HabilidadBase(BaseModel):
    nombre: str

class HabilidadCreate(HabilidadBase):
    pass

class Habilidad(HabilidadBase):
    id: int

    class Config:
        orm_mode = True

# Notificación schemas
class NotificacionBase(BaseModel):
    usuario_id: int
    mensaje: str
    leida: Optional[bool] = False

class NotificacionCreate(NotificacionBase):
    pass

class Notificacion(NotificacionBase):
    id: int
    fecha_envio: datetime

    class Config:
        orm_mode = True

# Mensaje schemas
class MensajeBase(BaseModel):
    emisor_id: int
    receptor_id: int
    contenido: str

class MensajeCreate(MensajeBase):
    pass

class Mensaje(MensajeBase):
    id: int
    fecha_envio: datetime

    class Config:
        orm_mode = True

# Evaluación schemas
class EvaluacionBase(BaseModel):
    postulacion_id: int
    evaluador_id: int
    comentario: Optional[str] = None
    puntaje: Optional[int] = None

class EvaluacionCreate(EvaluacionBase):
    pass

class Evaluacion(EvaluacionBase):
    id: int

    class Config:
        orm_mode = True

# Registro de Actividad schemas
class RegistroActividadBase(BaseModel):
    usuario_id: int
    accion: str

class RegistroActividadCreate(RegistroActividadBase):
    pass

class RegistroActividad(RegistroActividadBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True

# Token Blacklist schemas
class TokenBlacklistBase(BaseModel):
    token: str

class TokenBlacklistCreate(TokenBlacklistBase):
    pass

class TokenBlacklist(TokenBlacklistBase):
    id: int
    fecha_revocado: datetime

    class Config:
        orm_mode = True

# ----------------------
# CRUD ENDPOINTS
# ----------------------

# Rol endpoints
@app.post("/roles/", response_model=Rol, status_code=status.HTTP_201_CREATED, tags=["Roles"])
def create_rol(rol: RolCreate, db: Session = Depends(get_db)):
    """Crear un nuevo rol."""
    db_rol = models.Rol(nombre=rol.nombre)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

@app.get("/roles/", response_model=List[Rol], tags=["Roles"])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de roles."""
    roles = db.query(models.Rol).offset(skip).limit(limit).all()
    return roles

@app.get("/roles/{rol_id}", response_model=Rol, tags=["Roles"])
def read_rol(rol_id: int, db: Session = Depends(get_db)):
    """Obtener un rol por su ID."""
    db_rol = db.query(models.Rol).filter(models.Rol.id == rol_id).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_rol

@app.put("/roles/{rol_id}", response_model=Rol, tags=["Roles"])
def update_rol(rol_id: int, rol: RolCreate, db: Session = Depends(get_db)):
    """Actualizar un rol existente."""
    db_rol = db.query(models.Rol).filter(models.Rol.id == rol_id).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    db_rol.nombre = rol.nombre
    db.commit()
    db.refresh(db_rol)
    return db_rol

@app.delete("/roles/{rol_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Roles"])
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    """Eliminar un rol."""
    db_rol = db.query(models.Rol).filter(models.Rol.id == rol_id).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    db.delete(db_rol)
    db.commit()
    return None

# Usuario endpoints
@app.post("/usuarios/", response_model=Usuario, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario."""
    # En producción, hashear la contraseña aquí
    db_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        contraseña=usuario.contraseña,  # En producción: hashear la contraseña
        activo=usuario.activo,
        rol_id=usuario.rol_id
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/", response_model=List[Usuario], tags=["Usuarios"])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de usuarios."""
    usuarios = db.query(models.Usuario).offset(skip).limit(limit).all()
    return usuarios

@app.get("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por su ID."""
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
def update_usuario(usuario_id: int, usuario: UsuarioBase, db: Session = Depends(get_db)):
    """Actualizar un usuario existente."""
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar campos
    for key, value in usuario.dict().items():
        setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Eliminar un usuario."""
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return None

# Empresa endpoints
@app.post("/empresas/", response_model=Empresa, status_code=status.HTTP_201_CREATED, tags=["Empresas"])
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    """Crear una nueva empresa."""
    db_empresa = models.Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/", response_model=List[Empresa], tags=["Empresas"])
def read_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de empresas."""
    empresas = db.query(models.Empresa).offset(skip).limit(limit).all()
    return empresas

@app.get("/empresas/{empresa_id}", response_model=Empresa, tags=["Empresas"])
def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """Obtener una empresa por su ID."""
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa

@app.put("/empresas/{empresa_id}", response_model=Empresa, tags=["Empresas"])
def update_empresa(empresa_id: int, empresa: EmpresaBase, db: Session = Depends(get_db)):
    """Actualizar una empresa existente."""
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    # Actualizar campos
    for key, value in empresa.dict().items():
        setattr(db_empresa, key, value)
    
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.delete("/empresas/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Empresas"])
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """Eliminar una empresa."""
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    db.delete(empresa)
    db.commit()
    return None

# Postulante endpoints
@app.post("/postulantes/", response_model=Postulante, status_code=status.HTTP_201_CREATED, tags=["Postulantes"])
def create_postulante(postulante: PostulanteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo postulante."""
    db_postulante = models.Postulante(**postulante.dict())
    db.add(db_postulante)
    db.commit()
    db.refresh(db_postulante)
    return db_postulante

@app.get("/postulantes/", response_model=List[Postulante], tags=["Postulantes"])
def read_postulantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de postulantes."""
    postulantes = db.query(models.Postulante).offset(skip).limit(limit).all()
    return postulantes

@app.get("/postulantes/{postulante_id}", response_model=Postulante, tags=["Postulantes"])
def read_postulante(postulante_id: int, db: Session = Depends(get_db)):
    """Obtener un postulante por su ID."""
    postulante = db.query(models.Postulante).filter(models.Postulante.id == postulante_id).first()
    if postulante is None:
        raise HTTPException(status_code=404, detail="Postulante no encontrado")
    return postulante

@app.put("/postulantes/{postulante_id}", response_model=Postulante, tags=["Postulantes"])
def update_postulante(postulante_id: int, postulante: PostulanteBase, db: Session = Depends(get_db)):
    """Actualizar un postulante existente."""
    db_postulante = db.query(models.Postulante).filter(models.Postulante.id == postulante_id).first()
    if db_postulante is None:
        raise HTTPException(status_code=404, detail="Postulante no encontrado")
    
    # Actualizar campos
    for key, value in postulante.dict().items():
        setattr(db_postulante, key, value)
    
    db.commit()
    db.refresh(db_postulante)
    return db_postulante

@app.delete("/postulantes/{postulante_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Postulantes"])
def delete_postulante(postulante_id: int, db: Session = Depends(get_db)):
    """Eliminar un postulante."""
    postulante = db.query(models.Postulante).filter(models.Postulante.id == postulante_id).first()
    if postulante is None:
        raise HTTPException(status_code=404, detail="Postulante no encontrado")
    
    db.delete(postulante)
    db.commit()
    return None

# Categoría endpoints
@app.post("/categorias/", response_model=Categoria, status_code=status.HTTP_201_CREATED, tags=["Categorías"])
def create_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """Crear una nueva categoría."""
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.get("/categorias/", response_model=List[Categoria], tags=["Categorías"])
def read_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de categorías."""
    categorias = db.query(models.Categoria).offset(skip).limit(limit).all()
    return categorias

@app.get("/categorias/{categoria_id}", response_model=Categoria, tags=["Categorías"])
def read_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """Obtener una categoría por su ID."""
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@app.put("/categorias/{categoria_id}", response_model=Categoria, tags=["Categorías"])
def update_categoria(categoria_id: int, categoria: CategoriaBase, db: Session = Depends(get_db)):
    """Actualizar una categoría existente."""
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    db_categoria.nombre = categoria.nombre
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.delete("/categorias/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Categorías"])
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """Eliminar una categoría."""
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    db.delete(categoria)
    db.commit()
    return None

# Oferta Laboral endpoints
@app.post("/ofertas-laborales/", response_model=OfertaLaboral, status_code=status.HTTP_201_CREATED, tags=["Ofertas Laborales"])
def create_oferta_laboral(oferta: OfertaLaboralCreate, db: Session = Depends(get_db)):
    """Crear una nueva oferta laboral."""
    if not oferta.fecha_publicacion:
        oferta_dict = oferta.dict()
        oferta_dict["fecha_publicacion"] = date.today()
        db_oferta = models.OfertaLaboral(**oferta_dict)
    else:
        db_oferta = models.OfertaLaboral(**oferta.dict())
    
    db.add(db_oferta)
    db.commit()
    db.refresh(db_oferta)
    return db_oferta

@app.get("/ofertas-laborales/", response_model=List[OfertaLaboral], tags=["Ofertas Laborales"])
def read_ofertas_laborales(
    skip: int = 0, 
    limit: int = 100, 
    categoria_id: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de ofertas laborales.
    Opcionalmente filtrar por categoría y/o estado.
    """
    query = db.query(models.OfertaLaboral)
    
    if categoria_id:
        query = query.filter(models.OfertaLaboral.categoria_id == categoria_id)
    
    if estado:
        query = query.filter(models.OfertaLaboral.estado == estado)
    
    ofertas = query.offset(skip).limit(limit).all()
    return ofertas

@app.get("/ofertas-laborales/{oferta_id}", response_model=OfertaLaboral, tags=["Ofertas Laborales"])
def read_oferta_laboral(oferta_id: int, db: Session = Depends(get_db)):
    """Obtener una oferta laboral por su ID."""
    oferta = db.query(models.OfertaLaboral).filter(models.OfertaLaboral.id == oferta_id).first()
    if oferta is None:
        raise HTTPException(status_code=404, detail="Oferta laboral no encontrada")
    return oferta

@app.put("/ofertas-laborales/{oferta_id}", response_model=OfertaLaboral, tags=["Ofertas Laborales"])
def update_oferta_laboral(oferta_id: int, oferta: OfertaLaboralBase, db: Session = Depends(get_db)):
    """Actualizar una oferta laboral existente."""
    db_oferta = db.query(models.OfertaLaboral).filter(models.OfertaLaboral.id == oferta_id).first()
    if db_oferta is None:
        raise HTTPException(status_code=404, detail="Oferta laboral no encontrada")
    
    # Actualizar campos
    for key, value in oferta.dict().items():
        setattr(db_oferta, key, value)
    
    db.commit()
    db.refresh(db_oferta)
    return db_oferta

@app.delete("/ofertas-laborales/{oferta_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Ofertas Laborales"])
def delete_oferta_laboral(oferta_id: int, db: Session = Depends(get_db)):
    """Eliminar una oferta laboral."""
    oferta = db.query(models.OfertaLaboral).filter(models.OfertaLaboral.id == oferta_id).first()
    if oferta is None:
        raise HTTPException(status_code=404, detail="Oferta laboral no encontrada")
    
    db.delete(oferta)
    db.commit()
    return None

# Postulación endpoints
@app.post("/postulaciones/", response_model=Postulacion, status_code=status.HTTP_201_CREATED, tags=["Postulaciones"])
def create_postulacion(postulacion: PostulacionCreate, db: Session = Depends(get_db)):
    """Crear una nueva postulación."""
    if not postulacion.fecha_postulacion:
        postulacion_dict = postulacion.dict()
        postulacion_dict["fecha_postulacion"] = date.today()
        db_postulacion = models.Postulacion(**postulacion_dict)
    else:
        db_postulacion = models.Postulacion(**postulacion.dict())
    
    db.add(db_postulacion)
    db.commit()
    db.refresh(db_postulacion)
    return db_postulacion

@app.get("/postulaciones/", response_model=List[Postulacion], tags=["Postulaciones"])
def read_postulaciones(
    skip: int = 0, 
    limit: int = 100,
    postulante_id: Optional[int] = None,
    oferta_id: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de postulaciones.
    Opcionalmente filtrar por postulante, oferta y/o estado.
    """
    query = db.query(models.Postulacion)
    
    if postulante_id:
        query = query.filter(models.Postulacion.postulante_id == postulante_id)
    
    if oferta_id:
        query = query.filter(models.Postulacion.oferta_id == oferta_id)
    
    if estado:
        query = query.filter(models.Postulacion.estado == estado)
    
    postulaciones = query.offset(skip).limit(limit).all()
    return postulaciones

@app.get("/postulaciones/{postulacion_id}", response_model=Postulacion, tags=["Postulaciones"])
def read_postulacion(postulacion_id: int, db: Session = Depends(get_db)):
    """Obtener una postulación por su ID."""
    postulacion = db.query(models.Postulacion).filter(models.Postulacion.id == postulacion_id).first()
    if postulacion is None:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    return postulacion

@app.put("/postulaciones/{postulacion_id}", response_model=Postulacion, tags=["Postulaciones"])
def update_postulacion(postulacion_id: int, postulacion: PostulacionBase, db: Session = Depends(get_db)):
    """Actualizar una postulación existente."""
    db_postulacion = db.query(models.Postulacion).filter(models.Postulacion.id == postulacion_id).first()
    if db_postulacion is None:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    
    # Actualizar campos
    for key, value in postulacion.dict().items():
        setattr(db_postulacion, key, value)
    
    db.commit()
    db.refresh(db_postulacion)
    return db_postulacion

@app.delete("/postulaciones/{postulacion_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Postulaciones"])
def delete_postulacion(postulacion_id: int, db: Session = Depends(get_db)):
    """Eliminar una postulación."""
    postulacion = db.query(models.Postulacion).filter(models.Postulacion.id == postulacion_id).first()
    if postulacion is None:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    
    db.delete(postulacion)
    db.commit()
    return None

# Curriculum endpoints
@app.post("/curriculums/", response_model=Curriculum, status_code=status.HTTP_201_CREATED, tags=["Currículums"])
def create_curriculum(curriculum: CurriculumCreate, db: Session = Depends(get_db)):
    """Crear un nuevo currículum."""
    db_curriculum = models.Curriculum(**curriculum.dict())
    db.add(db_curriculum)
    db.commit()
    db.refresh(db_curriculum)
    return db_curriculum

@app.get("/curriculums/", response_model=List[Curriculum], tags=["Currículums"])
def read_curriculums(
    skip: int = 0, 
    limit: int = 100,
    postulante_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de currículums.
    Opcionalmente filtrar por postulante.
    """
    query = db.query(models.Curriculum)
    
    if postulante_id:
        query = query.filter(models.Curriculum.postulante_id == postulante_id)
    
    curriculums = query.offset(skip).limit(limit).all()
    return curriculums

@app.get("/curriculums/{curriculum_id}", response_model=Curriculum, tags=["Currículums"])
def read_curriculum(curriculum_id: int, db: Session = Depends(get_db)):
    """Obtener un currículum por su ID."""
    curriculum = db.query(models.Curriculum).filter(models.Curriculum.id == curriculum_id).first()
    if curriculum is None:
        raise HTTPException(status_code=404, detail="Currículum no encontrado")
    return curriculum

@app.put("/curriculums/{curriculum_id}", response_model=Curriculum, tags=["Currículums"])
def update_curriculum(curriculum_id: int, curriculum: CurriculumBase, db: Session = Depends(get_db)):
    """Actualizar un currículum existente."""
    db_curriculum = db.query(models.Curriculum).filter(models.Curriculum.id == curriculum_id).first()
    if db_curriculum is None:
        raise HTTPException(status_code=404, detail="Currículum no encontrado")
    
    # Actualizar campos
    for key, value in curriculum.dict().items():
        setattr(db_curriculum, key, value)
    
    db.commit()
    db.refresh(db_curriculum)
    return db_curriculum

@app.delete("/curriculums/{curriculum_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Currículums"])
def delete_curriculum(curriculum_id: int, db: Session = Depends(get_db)):
    """Eliminar un currículum."""
    curriculum = db.query(models.Curriculum).filter(models.Curriculum.id == curriculum_id).first()
    if curriculum is None:
        raise HTTPException(status_code=404, detail="Currículum no encontrado")
    
    db.delete(curriculum)
    db.commit()
    return None

# Educación endpoints
@app.post("/educaciones/", response_model=Educacion, status_code=status.HTTP_201_CREATED, tags=["Educación"])
def create_educacion(educacion: EducacionCreate, db: Session = Depends(get_db)):
    """Crear un nuevo registro de educación."""
    db_educacion = models.Educacion(**educacion.dict())
    db.add(db_educacion)
    db.commit()
    db.refresh(db_educacion)
    return db_educacion

@app.get("/educaciones/", response_model=List[Educacion], tags=["Educación"])
def read_educaciones(
    skip: int = 0, 
    limit: int = 100,
    curriculum_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de registros de educación.
    Opcionalmente filtrar por currículum.
    """
    query = db.query(models.Educacion)
    
    if curriculum_id:
        query = query.filter(models.Educacion.curriculum_id == curriculum_id)
    
    educaciones = query.offset(skip).limit(limit).all()
    return educaciones

@app.get("/educaciones/{educacion_id}", response_model=Educacion, tags=["Educación"])
def read_educacion(educacion_id: int, db: Session = Depends(get_db)):
    """Obtener un registro de educación por su ID."""
    educacion = db.query(models.Educacion).filter(models.Educacion.id == educacion_id).first()
    if educacion is None:
        raise HTTPException(status_code=404, detail="Registro de educación no encontrado")
    return educacion

@app.put("/educaciones/{educacion_id}", response_model=Educacion, tags=["Educación"])
def update_educacion(educacion_id: int, educacion: EducacionBase, db: Session = Depends(get_db)):
    """Actualizar un registro de educación existente."""
    db_educacion = db.query(models.Educacion).filter(models.Educacion.id == educacion_id).first()
    if db_educacion is None:
        raise HTTPException(status_code=404, detail="Registro de educación no encontrado")
    
    # Actualizar campos
    for key, value in educacion.dict().items():
        setattr(db_educacion, key, value)
    
    db.commit()
    db.refresh(db_educacion)
    return db_educacion

@app.delete("/educaciones/{educacion_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Educación"])
def delete_educacion(educacion_id: int, db: Session = Depends(get_db)):
    """Eliminar un registro de educación."""
    educacion = db.query(models.Educacion).filter(models.Educacion.id == educacion_id).first()
    if educacion is None:
        raise HTTPException(status_code=404, detail="Registro de educación no encontrado")
    
    db.delete(educacion)
    db.commit()
    return None

# Experiencia Laboral endpoints
@app.post("/experiencias-laborales/", response_model=ExperienciaLaboral, status_code=status.HTTP_201_CREATED, tags=["Experiencia Laboral"])
def create_experiencia_laboral(experiencia: ExperienciaLaboralCreate, db: Session = Depends(get_db)):
    """Crear un nuevo registro de experiencia laboral."""
    db_experiencia = models.ExperienciaLaboral(**experiencia.dict())
    db.add(db_experiencia)
    db.commit()
    db.refresh(db_experiencia)
    return db_experiencia

@app.get("/experiencias-laborales/", response_model=List[ExperienciaLaboral], tags=["Experiencia Laboral"])
def read_experiencias_laborales(
    skip: int = 0, 
    limit: int = 100,
    curriculum_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de registros de experiencia laboral.
    Opcionalmente filtrar por currículum.
    """
    query = db.query(models.ExperienciaLaboral)
    
    if curriculum_id:
        query = query.filter(models.ExperienciaLaboral.curriculum_id == curriculum_id)
    
    experiencias = query.offset(skip).limit(limit).all()
    return experiencias

@app.get("/experiencias-laborales/{experiencia_id}", response_model=ExperienciaLaboral, tags=["Experiencia Laboral"])
def read_experiencia_laboral(experiencia_id: int, db: Session = Depends(get_db)):
    """Obtener un registro de experiencia laboral por su ID."""
    experiencia = db.query(models.ExperienciaLaboral).filter(models.ExperienciaLaboral.id == experiencia_id).first()
    if experiencia is None:
        raise HTTPException(status_code=404, detail="Registro de experiencia laboral no encontrado")
    return experiencia

@app.put("/experiencias-laborales/{experiencia_id}", response_model=ExperienciaLaboral, tags=["Experiencia Laboral"])
def update_experiencia_laboral(experiencia_id: int, experiencia: ExperienciaLaboralBase, db: Session = Depends(get_db)):
    """Actualizar un registro de experiencia laboral existente."""
    db_experiencia = db.query(models.ExperienciaLaboral).filter(models.ExperienciaLaboral.id == experiencia_id).first()
    if db_experiencia is None:
        raise HTTPException(status_code=404, detail="Registro de experiencia laboral no encontrado")
    
    # Actualizar campos
    for key, value in experiencia.dict().items():
        setattr(db_experiencia, key, value)
    
    db.commit()
    db.refresh(db_experiencia)
    return db_experiencia

@app.delete("/experiencias-laborales/{experiencia_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Experiencia Laboral"])
def delete_experiencia_laboral(experiencia_id: int, db: Session = Depends(get_db)):
    """Eliminar un registro de experiencia laboral."""
    experiencia = db.query(models.ExperienciaLaboral).filter(models.ExperienciaLaboral.id == experiencia_id).first()
    if experiencia is None:
        raise HTTPException(status_code=404, detail="Registro de experiencia laboral no encontrado")
    
    db.delete(experiencia)
    db.commit()
    return None

# Entrevista endpoints
@app.post("/entrevistas/", response_model=Entrevista, status_code=status.HTTP_201_CREATED, tags=["Entrevistas"])
def create_entrevista(entrevista: EntrevistaCreate, db: Session = Depends(get_db)):
    """Crear una nueva entrevista."""
    db_entrevista = models.Entrevista(**entrevista.dict())
    db.add(db_entrevista)
    db.commit()
    db.refresh(db_entrevista)
    return db_entrevista

@app.get("/entrevistas/", response_model=List[Entrevista], tags=["Entrevistas"])
def read_entrevistas(
    skip: int = 0, 
    limit: int = 100,
    postulacion_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de entrevistas.
    Opcionalmente filtrar por postulación.
    """
    query = db.query(models.Entrevista)
    
    if postulacion_id:
        query = query.filter(models.Entrevista.postulacion_id == postulacion_id)
    
    entrevistas = query.offset(skip).limit(limit).all()
    return entrevistas

@app.get("/entrevistas/{entrevista_id}", response_model=Entrevista, tags=["Entrevistas"])
def read_entrevista(entrevista_id: int, db: Session = Depends(get_db)):
    """Obtener una entrevista por su ID."""
    entrevista = db.query(models.Entrevista).filter(models.Entrevista.id == entrevista_id).first()
    if entrevista is None:
        raise HTTPException(status_code=404, detail="Entrevista no encontrada")
    return entrevista

@app.put("/entrevistas/{entrevista_id}", response_model=Entrevista, tags=["Entrevistas"])
def update_entrevista(entrevista_id: int, entrevista: EntrevistaBase, db: Session = Depends(get_db)):
    """Actualizar una entrevista existente."""
    db_entrevista = db.query(models.Entrevista).filter(models.Entrevista.id == entrevista_id).first()
    if db_entrevista is None:
        raise HTTPException(status_code=404, detail="Entrevista no encontrada")
    
    # Actualizar campos
    for key, value in entrevista.dict().items():
        setattr(db_entrevista, key, value)
    
    db.commit()
    db.refresh(db_entrevista)
    return db_entrevista

@app.delete("/entrevistas/{entrevista_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Entrevistas"])
def delete_entrevista(entrevista_id: int, db: Session = Depends(get_db)):
    """Eliminar una entrevista."""
    entrevista = db.query(models.Entrevista).filter(models.Entrevista.id == entrevista_id).first()
    if entrevista is None:
        raise HTTPException(status_code=404, detail="Entrevista no encontrada")
    
    db.delete(entrevista)
    db.commit()
    return None

# Habilidad endpoints
@app.post("/habilidades/", response_model=Habilidad, status_code=status.HTTP_201_CREATED, tags=["Habilidades"])
def create_habilidad(habilidad: HabilidadCreate, db: Session = Depends(get_db)):
    """Crear una nueva habilidad."""
    db_habilidad = models.Habilidad(**habilidad.dict())
    db.add(db_habilidad)
    db.commit()
    db.refresh(db_habilidad)
    return db_habilidad

@app.get("/habilidades/", response_model=List[Habilidad], tags=["Habilidades"])
def read_habilidades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de habilidades."""
    habilidades = db.query(models.Habilidad).offset(skip).limit(limit).all()
    return habilidades

@app.get("/habilidades/{habilidad_id}", response_model=Habilidad, tags=["Habilidades"])
def read_habilidad(habilidad_id: int, db: Session = Depends(get_db)):
    """Obtener una habilidad por su ID."""
    habilidad = db.query(models.Habilidad).filter(models.Habilidad.id == habilidad_id).first()
    if habilidad is None:
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")
    return habilidad

@app.put("/habilidades/{habilidad_id}", response_model=Habilidad, tags=["Habilidades"])
def update_habilidad(habilidad_id: int, habilidad: HabilidadBase, db: Session = Depends(get_db)):
    """Actualizar una habilidad existente."""
    db_habilidad = db.query(models.Habilidad).filter(models.Habilidad.id == habilidad_id).first()
    if db_habilidad is None:
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")
    
    db_habilidad.nombre = habilidad.nombre
    db.commit()
    db.refresh(db_habilidad)
    return db_habilidad

@app.delete("/habilidades/{habilidad_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Habilidades"])
def delete_habilidad(habilidad_id: int, db: Session = Depends(get_db)):
    """Eliminar una habilidad."""
    habilidad = db.query(models.Habilidad).filter(models.Habilidad.id == habilidad_id).first()
    if habilidad is None:
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")
    
    db.delete(habilidad)
    db.commit()
    return None
# Notificación endpoints
@app.post("/notificaciones/", response_model=Notificacion, status_code=status.HTTP_201_CREATED, tags=["Notificaciones"])
def create_notificacion(notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    """Crear una nueva notificación."""
    db_notificacion = models.Notificacion(**notificacion.dict())
    db.add(db_notificacion)
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion

@app.get("/notificaciones/", response_model=List[Notificacion], tags=["Notificaciones"])
def read_notificaciones(
    skip: int = 0, 
    limit: int = 100,
    usuario_id: Optional[int] = None,
    leida: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de notificaciones.
    Opcionalmente filtrar por usuario y/o estado de lectura.
    """
    query = db.query(models.Notificacion)
    
    if usuario_id:
        query = query.filter(models.Notificacion.usuario_id == usuario_id)
    
    if leida is not None:
        query = query.filter(models.Notificacion.leida == leida)
    
    notificaciones = query.offset(skip).limit(limit).all()
    return notificaciones

@app.get("/notificaciones/{notificacion_id}", response_model=Notificacion, tags=["Notificaciones"])
def read_notificacion(notificacion_id: int, db: Session = Depends(get_db)):
    """Obtener una notificación por su ID."""
    notificacion = db.query(models.Notificacion).filter(models.Notificacion.id == notificacion_id).first()
    if notificacion is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return notificacion

@app.put("/notificaciones/{notificacion_id}", response_model=Notificacion, tags=["Notificaciones"])
def update_notificacion(notificacion_id: int, notificacion: NotificacionBase, db: Session = Depends(get_db)):
    """Actualizar una notificación existente."""
    db_notificacion = db.query(models.Notificacion).filter(models.Notificacion.id == notificacion_id).first()
    if db_notificacion is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    
    # Actualizar campos
    for key, value in notificacion.dict().items():
        setattr(db_notificacion, key, value)
    
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion

@app.delete("/notificaciones/{notificacion_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Notificaciones"])
def delete_notificacion(notificacion_id: int, db: Session = Depends(get_db)):
    """Eliminar una notificación."""
    notificacion = db.query(models.Notificacion).filter(models.Notificacion.id == notificacion_id).first()
    if notificacion is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    
    db.delete(notificacion)
    db.commit()
    return None

# Mensaje endpoints
@app.post("/mensajes/", response_model=Mensaje, status_code=status.HTTP_201_CREATED, tags=["Mensajes"])
def create_mensaje(mensaje: MensajeCreate, db: Session = Depends(get_db)):
    """Crear un nuevo mensaje."""
    db_mensaje = models.Mensaje(**mensaje.dict())
    db.add(db_mensaje)
    db.commit()
    db.refresh(db_mensaje)
    return db_mensaje

@app.get("/mensajes/", response_model=List[Mensaje], tags=["Mensajes"])
def read_mensajes(
    skip: int = 0, 
    limit: int = 100,
    emisor_id: Optional[int] = None,
    receptor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de mensajes.
    Opcionalmente filtrar por emisor y/o receptor.
    """
    query = db.query(models.Mensaje)
    
    if emisor_id:
        query = query.filter(models.Mensaje.emisor_id == emisor_id)
    
    if receptor_id:
        query = query.filter(models.Mensaje.receptor_id == receptor_id)
    
    mensajes = query.offset(skip).limit(limit).all()
    return mensajes

@app.get("/mensajes/{mensaje_id}", response_model=Mensaje, tags=["Mensajes"])
def read_mensaje(mensaje_id: int, db: Session = Depends(get_db)):
    """Obtener un mensaje por su ID."""
    mensaje = db.query(models.Mensaje).filter(models.Mensaje.id == mensaje_id).first()
    if mensaje is None:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return mensaje

@app.put("/mensajes/{mensaje_id}", response_model=Mensaje, tags=["Mensajes"])
def update_mensaje(mensaje_id: int, mensaje: MensajeBase, db: Session = Depends(get_db)):
    """Actualizar un mensaje existente."""
    db_mensaje = db.query(models.Mensaje).filter(models.Mensaje.id == mensaje_id).first()
    if db_mensaje is None:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    # Actualizar campos
    for key, value in mensaje.dict().items():
        setattr(db_mensaje, key, value)
    
    db.commit()
    db.refresh(db_mensaje)
    return db_mensaje

@app.delete("/mensajes/{mensaje_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Mensajes"])
def delete_mensaje(mensaje_id: int, db: Session = Depends(get_db)):
    """Eliminar un mensaje."""
    mensaje = db.query(models.Mensaje).filter(models.Mensaje.id == mensaje_id).first()
    if mensaje is None:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    db.delete(mensaje)
    db.commit()
    return None

# Evaluación endpoints
@app.post("/evaluaciones/", response_model=Evaluacion, status_code=status.HTTP_201_CREATED, tags=["Evaluaciones"])
def create_evaluacion(evaluacion: EvaluacionCreate, db: Session = Depends(get_db)):
    """Crear una nueva evaluación."""
    db_evaluacion = models.Evaluacion(**evaluacion.dict())
    db.add(db_evaluacion)
    db.commit()
    db.refresh(db_evaluacion)
    return db_evaluacion

@app.get("/evaluaciones/", response_model=List[Evaluacion], tags=["Evaluaciones"])
def read_evaluaciones(
    skip: int = 0, 
    limit: int = 100,
    postulacion_id: Optional[int] = None,
    evaluador_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de evaluaciones.
    Opcionalmente filtrar por postulación y/o evaluador.
    """
    query = db.query(models.Evaluacion)
    
    if postulacion_id:
        query = query.filter(models.Evaluacion.postulacion_id == postulacion_id)
    
    if evaluador_id:
        query = query.filter(models.Evaluacion.evaluador_id == evaluador_id)
    
    evaluaciones = query.offset(skip).limit(limit).all()
    return evaluaciones

@app.get("/evaluaciones/{evaluacion_id}", response_model=Evaluacion, tags=["Evaluaciones"])
def read_evaluacion(evaluacion_id: int, db: Session = Depends(get_db)):
    """Obtener una evaluación por su ID."""
    evaluacion = db.query(models.Evaluacion).filter(models.Evaluacion.id == evaluacion_id).first()
    if evaluacion is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return evaluacion

@app.put("/evaluaciones/{evaluacion_id}", response_model=Evaluacion, tags=["Evaluaciones"])
def update_evaluacion(evaluacion_id: int, evaluacion: EvaluacionBase, db: Session = Depends(get_db)):
    """Actualizar una evaluación existente."""
    db_evaluacion = db.query(models.Evaluacion).filter(models.Evaluacion.id == evaluacion_id).first()
    if db_evaluacion is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    # Actualizar campos
    for key, value in evaluacion.dict().items():
        setattr(db_evaluacion, key, value)
    
    db.commit()
    db.refresh(db_evaluacion)
    return db_evaluacion

@app.delete("/evaluaciones/{evaluacion_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Evaluaciones"])
def delete_evaluacion(evaluacion_id: int, db: Session = Depends(get_db)):
    """Eliminar una evaluación."""
    evaluacion = db.query(models.Evaluacion).filter(models.Evaluacion.id == evaluacion_id).first()
    if evaluacion is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    db.delete(evaluacion)
    db.commit()
    return None

# Registro de Actividad endpoints
@app.post("/registros-actividad/", response_model=RegistroActividad, status_code=status.HTTP_201_CREATED, tags=["Registros de Actividad"])
def create_registro_actividad(registro: RegistroActividadCreate, db: Session = Depends(get_db)):
    """Crear un nuevo registro de actividad."""
    db_registro = models.RegistroActividad(**registro.dict())
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro

@app.get("/registros-actividad/", response_model=List[RegistroActividad], tags=["Registros de Actividad"])
def read_registros_actividad(
    skip: int = 0, 
    limit: int = 100,
    usuario_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de registros de actividad.
    Opcionalmente filtrar por usuario.
    """
    query = db.query(models.RegistroActividad)
    
    if usuario_id:
        query = query.filter(models.RegistroActividad.usuario_id == usuario_id)
    
    registros = query.offset(skip).limit(limit).all()
    return registros

@app.get("/registros-actividad/{registro_id}", response_model=RegistroActividad, tags=["Registros de Actividad"])
def read_registro_actividad(registro_id: int, db: Session = Depends(get_db)):
    """Obtener un registro de actividad por su ID."""
    registro = db.query(models.RegistroActividad).filter(models.RegistroActividad.id == registro_id).first()
    if registro is None:
        raise HTTPException(status_code=404, detail="Registro de actividad no encontrado")
    return registro

@app.delete("/registros-actividad/{registro_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Registros de Actividad"])
def delete_registro_actividad(registro_id: int, db: Session = Depends(get_db)):
    """Eliminar un registro de actividad."""
    registro = db.query(models.RegistroActividad).filter(models.RegistroActividad.id == registro_id).first()
    if registro is None:
        raise HTTPException(status_code=404, detail="Registro de actividad no encontrado")
    
    db.delete(registro)
    db.commit()
    return None

# Token Blacklist endpoints
@app.post("/token-blacklist/", response_model=TokenBlacklist, status_code=status.HTTP_201_CREATED, tags=["Token Blacklist"])
def create_token_blacklist(token: TokenBlacklistCreate, db: Session = Depends(get_db)):
    """Añadir un token a la lista negra."""
    db_token = models.TokenBlacklist(**token.dict())
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

@app.get("/token-blacklist/", response_model=List[TokenBlacklist], tags=["Token Blacklist"])
def read_token_blacklist(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de tokens en la lista negra."""
    tokens = db.query(models.TokenBlacklist).offset(skip).limit(limit).all()
    return tokens

@app.get("/token-blacklist/{token_id}", response_model=TokenBlacklist, tags=["Token Blacklist"])
def read_token_blacklist_by_id(token_id: int, db: Session = Depends(get_db)):
    """Obtener un token de la lista negra por su ID."""
    token = db.query(models.TokenBlacklist).filter(models.TokenBlacklist.id == token_id).first()
    if token is None:
        raise HTTPException(status_code=404, detail="Token no encontrado")
    return token

@app.get("/token-blacklist/check/{token_value}", tags=["Token Blacklist"])
def check_token_in_blacklist(token_value: str, db: Session = Depends(get_db)):
    """Verificar si un token está en la lista negra."""
    token = db.query(models.TokenBlacklist).filter(models.TokenBlacklist.token == token_value).first()
    return {"is_blacklisted": token is not None}
# Endpoints adicionales útiles

# Endpoint para obtener ofertas laborales por empresa
@app.get("/empresas/{empresa_id}/ofertas-laborales/", response_model=List[OfertaLaboral], tags=["Empresas", "Ofertas Laborales"])
def read_ofertas_laborales_by_empresa(
    empresa_id: int, 
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener todas las ofertas laborales de una empresa específica."""
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    query = db.query(models.OfertaLaboral).filter(models.OfertaLaboral.empresa_id == empresa_id)
    
    if estado:
        query = query.filter(models.OfertaLaboral.estado == estado)
    
    ofertas = query.offset(skip).limit(limit).all()
    return ofertas

# Endpoint para obtener postulaciones por postulante
@app.get("/postulantes/{postulante_id}/postulaciones/", response_model=List[Postulacion], tags=["Postulantes", "Postulaciones"])
def read_postulaciones_by_postulante(
    postulante_id: int, 
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener todas las postulaciones de un postulante específico."""
    postulante = db.query(models.Postulante).filter(models.Postulante.id == postulante_id).first()
    if postulante is None:
        raise HTTPException(status_code=404, detail="Postulante no encontrado")
    
    query = db.query(models.Postulacion).filter(models.Postulacion.postulante_id == postulante_id)
    
    if estado:
        query = query.filter(models.Postulacion.estado == estado)
    
    postulaciones = query.offset(skip).limit(limit).all()
    return postulaciones

# Endpoint para obtener entrevistas por postulación
@app.get("/postulaciones/{postulacion_id}/entrevistas/", response_model=List[Entrevista], tags=["Postulaciones", "Entrevistas"])
def read_entrevistas_by_postulacion(
    postulacion_id: int, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todas las entrevistas de una postulación específica."""
    postulacion = db.query(models.Postulacion).filter(models.Postulacion.id == postulacion_id).first()
    if postulacion is None:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    
    entrevistas = db.query(models.Entrevista).filter(
        models.Entrevista.postulacion_id == postulacion_id
    ).offset(skip).limit(limit).all()
    
    return entrevistas

# Endpoint para obtener evaluaciones por postulación
@app.get("/postulaciones/{postulacion_id}/evaluaciones/", response_model=List[Evaluacion], tags=["Postulaciones", "Evaluaciones"])
def read_evaluaciones_by_postulacion(
    postulacion_id: int, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todas las evaluaciones de una postulación específica."""
    postulacion = db.query(models.Postulacion).filter(models.Postulacion.id == postulacion_id).first()
    if postulacion is None:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    
    evaluaciones = db.query(models.Evaluacion).filter(
        models.Evaluacion.postulacion_id == postulacion_id
    ).offset(skip).limit(limit).all()
    
    return evaluaciones

# Endpoint para obtener currículum por postulante
@app.get("/postulantes/{postulante_id}/curriculum/", response_model=List[Curriculum], tags=["Postulantes", "Currículums"])
def read_curriculum_by_postulante(
    postulante_id: int, 
    db: Session = Depends(get_db)
):
    """Obtener todos los currículums de un postulante específico."""
    postulante = db.query(models.Postulante).filter(models.Postulante.id == postulante_id).first()
    if postulante is None:
        raise HTTPException(status_code=404, detail="Postulante no encontrado")
    
    curriculums = db.query(models.Curriculum).filter(
        models.Curriculum.postulante_id == postulante_id
    ).all()
    
    return curriculums

# Endpoint para obtener educación por currículum
@app.get("/curriculums/{curriculum_id}/educaciones/", response_model=List[Educacion], tags=["Currículums", "Educación"])
def read_educaciones_by_curriculum(
    curriculum_id: int, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los registros de educación de un currículum específico."""
    curriculum = db.query(models.Curriculum).filter(models.Curriculum.id == curriculum_id).first()
    if curriculum is None:
        raise HTTPException(status_code=404, detail="Currículum no encontrado")
    
    educaciones = db.query(models.Educacion).filter(
        models.Educacion.curriculum_id == curriculum_id
    ).offset(skip).limit(limit).all()
    
    return educaciones

# Endpoint para obtener experiencias laborales por currículum
@app.get("/curriculums/{curriculum_id}/experiencias-laborales/", response_model=List[ExperienciaLaboral], tags=["Currículums", "Experiencia Laboral"])
def read_experiencias_by_curriculum(
    curriculum_id: int, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los registros de experiencia laboral de un currículum específico."""
    curriculum = db.query(models.Curriculum).filter(models.Curriculum.id == curriculum_id).first()
    if curriculum is None:
        raise HTTPException(status_code=404, detail="Currículum no encontrado")
    
    experiencias = db.query(models.ExperienciaLaboral).filter(
        models.ExperienciaLaboral.curriculum_id == curriculum_id
    ).offset(skip).limit(limit).all()
    
    return experiencias

# Endpoint para obtener notificaciones por usuario
@app.get("/usuarios/{usuario_id}/notificaciones/", response_model=List[Notificacion], tags=["Usuarios", "Notificaciones"])
def read_notificaciones_by_usuario(
    usuario_id: int, 
    skip: int = 0, 
    limit: int = 100,
    leida: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Obtener todas las notificaciones de un usuario específico."""
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    query = db.query(models.Notificacion).filter(models.Notificacion.usuario_id == usuario_id)
    
    if leida is not None:
        query = query.filter(models.Notificacion.leida == leida)
    
    notificaciones = query.offset(skip).limit(limit).all()
    return notificaciones

# Endpoint para obtener mensajes entre dos usuarios
@app.get("/mensajes/entre-usuarios/", response_model=List[Mensaje], tags=["Mensajes"])
def read_mensajes_entre_usuarios(
    usuario1_id: int,
    usuario2_id: int,
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los mensajes intercambiados entre dos usuarios específicos."""
    # Verificar que ambos usuarios existen
    usuario1 = db.query(models.Usuario).filter(models.Usuario.id == usuario1_id).first()
    usuario2 = db.query(models.Usuario).filter(models.Usuario.id == usuario2_id).first()
    
    if usuario1 is None or usuario2 is None:
        raise HTTPException(status_code=404, detail="Uno o ambos usuarios no encontrados")
    
    # Obtener mensajes en ambas direcciones
    mensajes = db.query(models.Mensaje).filter(
        ((models.Mensaje.emisor_id == usuario1_id) & (models.Mensaje.receptor_id == usuario2_id)) |
        ((models.Mensaje.emisor_id == usuario2_id) & (models.Mensaje.receptor_id == usuario1_id))
    ).order_by(models.Mensaje.fecha_envio).offset(skip).limit(limit).all()
    
    return mensajes

# Endpoint para obtener postulantes por oferta laboral
@app.get("/ofertas-laborales/{oferta_id}/postulantes/", tags=["Ofertas Laborales", "Postulantes"])
def read_postulantes_by_oferta(
    oferta_id: int, 
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener todos los postulantes que han aplicado a una oferta laboral específica."""
    oferta = db.query(models.OfertaLaboral).filter(models.OfertaLaboral.id == oferta_id).first()
    if oferta is None:
        raise HTTPException(status_code=404, detail="Oferta laboral no encontrada")
    
    # Construir la consulta base para las postulaciones
    query = db.query(models.Postulacion).filter(models.Postulacion.oferta_id == oferta_id)
    
    # Filtrar por estado si se especifica
    if estado:
        query = query.filter(models.Postulacion.estado == estado)
    
    # Obtener las postulaciones
    postulaciones = query.offset(skip).limit(limit).all()
    
    # Obtener los IDs de los postulantes
    postulante_ids = [p.postulante_id for p in postulaciones]
    
    # Obtener los objetos postulante
    postulantes = db.query(models.Postulante).filter(models.Postulante.id.in_(postulante_ids)).all()
    
    # Crear un diccionario para almacenar información de los postulantes con su estado de postulación
    result = []
    for postulante in postulantes:
        # Encontrar la postulación correspondiente
        postulacion = next((p for p in postulaciones if p.postulante_id == postulante.id), None)
        
        # Crear objeto de respuesta
        postulante_info = {
            "id": postulante.id,
            "nombre_completo": postulante.nombre_completo,
            "telefono": postulante.telefono,
            "postulacion_id": postulacion.id if postulacion else None,
            "estado_postulacion": postulacion.estado if postulacion else None,
            "fecha_postulacion": postulacion.fecha_postulacion if postulacion else None
        }
        result.append(postulante_info)
    
    return result

# Endpoint para marcar una notificación como leída
@app.put("/notificaciones/{notificacion_id}/leer", response_model=Notificacion, tags=["Notificaciones"])
def marcar_notificacion_como_leida(notificacion_id: int, db: Session = Depends(get_db)):
    """Marcar una notificación específica como leída."""
    notificacion = db.query(models.Notificacion).filter(models.Notificacion.id == notificacion_id).first()
    if notificacion is None:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    
    notificacion.leida = True
    db.commit()
    db.refresh(notificacion)
    return notificacion

# Endpoint para marcar todas las notificaciones de un usuario como leídas
@app.put("/usuarios/{usuario_id}/notificaciones/leer-todas", tags=["Usuarios", "Notificaciones"])
def marcar_todas_notificaciones_como_leidas(usuario_id: int, db: Session = Depends(get_db)):
    """Marcar todas las notificaciones de un usuario específico como leídas."""
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar todas las notificaciones no leídas
    result = db.query(models.Notificacion).filter(
        models.Notificacion.usuario_id == usuario_id,
        models.Notificacion.leida == False
    ).update({"leida": True})
    
    db.commit()
    return {"mensaje": f"Se han marcado {result} notificaciones como leídas"}

# Endpoint para actualizar el estado de una postulación
@app.put("/postulaciones/{postulacion_id}/actualizar-estado", response_model=Postulacion, tags=["Postulaciones"])
def actualizar_estado_postulacion(
    postulacion_id: int, 
    estado: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """Actualizar el estado de una postulación específica."""
    postulacion = db.query(models.Postulacion).filter(models.Postulacion.id == postulacion_id).first()
    if postulacion is None:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    
    # Validar el estado (puedes agregar más validaciones según tus necesidades)
    estados_validos = ["pendiente", "revisada", "entrevista", "aceptada", "rechazada"]
    if estado not in estados_validos:
        raise HTTPException(
            status_code=400, 
            detail=f"Estado no válido. Los estados válidos son: {', '.join(estados_validos)}"
        )
    
    postulacion.estado = estado
    db.commit()
    db.refresh(postulacion)
    return postulacion

# Endpoint para actualizar el estado de una oferta laboral
@app.put("/ofertas-laborales/{oferta_id}/actualizar-estado", response_model=OfertaLaboral, tags=["Ofertas Laborales"])
def actualizar_estado_oferta(
    oferta_id: int, 
    estado: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """Actualizar el estado de una oferta laboral específica."""
    oferta = db.query(models.OfertaLaboral).filter(models.OfertaLaboral.id == oferta_id).first()
    if oferta is None:
        raise HTTPException(status_code=404, detail="Oferta laboral no encontrada")
    
    # Validar el estado
    estados_validos = ["activa", "cerrada", "pausada", "eliminada"]
    if estado not in estados_validos:
        raise HTTPException(
            status_code=400, 
            detail=f"Estado no válido. Los estados válidos son: {', '.join(estados_validos)}"
        )
    
    oferta.estado = estado
    db.commit()
    db.refresh(oferta)
    return oferta

# Punto de entrada para iniciar la aplicación
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)