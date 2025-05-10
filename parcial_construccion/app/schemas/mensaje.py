from pydantic import BaseModel
from datetime import datetime

class MensajeBase(BaseModel):
    emisor_id: int
    receptor_id: int
    contenido: str
    fecha_envio: datetime = None

    class Config:
        orm_mode = True

class MensajeCreate(MensajeBase):
    pass

class MensajeOut(MensajeBase):
    id: int
