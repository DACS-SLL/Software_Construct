from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.models.token import TokenBlacklist
from app.core.security import ALGORITHM, SECRET_KEY
from typing import List, Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verificar si el token está en la lista negra
    blacklisted = db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first()
    if blacklisted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revocado o sesión cerrada",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise credentials_exception
    
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return usuario

def require_role(roles: List[str] = None):
    if roles is None:
        roles = []
    
    def _require_role(usuario_actual: Usuario = Depends(get_current_user)):
        if not roles:
            return usuario_actual
        
        if usuario_actual.rol.nombre not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"El rol {usuario_actual.rol.nombre} no tiene permisos para realizar esta acción"
            )
        
        return usuario_actual
    
    return _require_role