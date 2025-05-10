
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .postulacion import PostulacionOut

class EntrevistaBase(BaseModel):
    postulacion_id: int
    fecha: datetime
    modalidad: str
    resultado: Optional[str] = None

class EntrevistaCreate(EntrevistaBase):
    pass

class EntrevistaUpdate(EntrevistaBase):
    pass

class EntrevistaOut(EntrevistaBase):
    id: int
    postulacion: PostulacionOut

    class Config:
        orm_mode = True
