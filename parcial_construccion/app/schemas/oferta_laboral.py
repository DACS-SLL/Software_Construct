from pydantic import BaseModel
from datetime import date
from typing import Optional
from .categoria import CategoriaOut

class OfertaLaboralBase(BaseModel):
    titulo: str
    descripcion: str
    ubicacion: str
    fecha_publicacion: date
    estado: str
    categoria_id: int
    empresa_id: int

    class Config:
        orm_mode = True

class OfertaLaboralCreate(OfertaLaboralBase):
    pass

class OfertaLaboralUpdate(OfertaLaboralBase):
    pass

class OfertaLaboralOut(OfertaLaboralBase):
    id: int
    categoria: CategoriaOut

    class Config:
        orm_mode = True
