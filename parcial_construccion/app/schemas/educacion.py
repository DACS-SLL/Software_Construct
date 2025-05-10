from pydantic import BaseModel
from datetime import date
from typing import Optional
from .curriculum import CurriculumOut

class EducacionBase(BaseModel):
    curriculum_id: int
    institucion: str
    titulo: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None

class EducacionCreate(EducacionBase):
    pass

class EducacionUpdate(EducacionBase):
    pass

class EducacionOut(EducacionBase):
    id: int
    curriculum: CurriculumOut

    class Config:
        orm_mode = True