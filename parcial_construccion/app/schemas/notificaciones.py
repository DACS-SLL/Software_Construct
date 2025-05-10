from pydantic import BaseModel
from datetime import datetime

class NotificacionBase(BaseModel):
    usuario_id: int
    mensaje: str
    leida: bool = False
    fecha_envio: datetime = None

    class Config:
        orm_mode = True

class NotificacionCreate(NotificacionBase):
    pass

class NotificacionOut(NotificacionBase):
    id: int
