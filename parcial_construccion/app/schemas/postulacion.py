from pydantic import BaseModel
from datetime import date
from typing import Optional

class PostulacionBase(BaseModel):
    postulante_id: int
    oferta_id: int
    fecha_postulacion: date
    estado: str

class PostulacionCreate(PostulacionBase):
    pass

class PostulacionUpdate(PostulacionBase):
    pass

class PostulacionOut(PostulacionBase):
    id: int

    class Config:
        orm_mode = True