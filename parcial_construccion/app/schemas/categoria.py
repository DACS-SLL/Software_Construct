from pydantic import BaseModel
from typing import Optional

class CategoriaBase(BaseModel):
    nombre: str

    class Config:
        orm_mode = True

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    pass

class CategoriaOut(CategoriaBase):
    id: int

    class Config:
        orm_mode = True
