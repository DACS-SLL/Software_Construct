from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    credentials_exception = HTTPException(status_code=401, detail="Token inválido", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None or not usuario.activo:
        raise credentials_exception

    return usuario

def require_role(roles: List[str]):
    def role_checker(usuario: Usuario = Depends(get_current_user)):
        if usuario.rol.nombre not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Acceso denegado. Se requiere uno de los roles: {roles}"
            )
        return usuario
    return role_checker
