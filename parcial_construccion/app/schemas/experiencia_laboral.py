from pydantic import BaseModel
from datetime import date
from typing import Optional
from .curriculum import CurriculumOut

class ExperienciaLaboralBase(BaseModel):
    curriculum_id: int
    empresa: str
    cargo: str
    descripcion: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None

class ExperienciaLaboralCreate(ExperienciaLaboralBase):
    pass

class ExperienciaLaboralUpdate(ExperienciaLaboralBase):
    pass

class ExperienciaLaboralOut(ExperienciaLaboralBase):
    id: int
    curriculum: CurriculumOut

    class Config:
        orm_mode = True