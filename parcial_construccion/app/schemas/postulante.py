from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from .auth import UsuarioOut

class PostulanteCreate(BaseModel):
    usuario_id: int
    nombre_completo: str
    fecha_nacimiento: date
    telefono: str

class CurriculumOut(BaseModel):
    id: int
    descripcion: str
    fecha_creacion: date

    class Config:
        orm_mode = True

class PostulanteOut(PostulanteCreate):
    id: int
    usuario: Optional[UsuarioOut] 
    curriculum: Optional[list[CurriculumOut]] 

    class Config:
        orm_mode = True
