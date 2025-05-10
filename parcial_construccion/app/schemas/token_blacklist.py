from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TokenBlacklistBase(BaseModel):
    token: str

class TokenBlacklistCreate(TokenBlacklistBase):
    pass

class TokenBlacklistResponse(TokenBlacklistBase):
    id: int
    fecha_revocado: datetime
    
    class Config:
        orm_mode = True