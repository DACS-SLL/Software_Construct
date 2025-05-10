from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CurriculumBase(BaseModel):
    postulante_id: int
    ruta_archivo: str
    fecha_subida: Optional[datetime] = None

class CurriculumCreate(CurriculumBase):
    pass

class CurriculumUpdate(CurriculumBase):
    pass

class CurriculumOut(CurriculumBase):
    id: int
    fecha_subida: datetime


    class Config:
        orm_mode = True