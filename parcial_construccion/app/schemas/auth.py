from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol_id: int

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol_id: int
    activo: bool

    class Config:
        orm_mode = True

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
