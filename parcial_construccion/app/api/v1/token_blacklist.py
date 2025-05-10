from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.token_blacklist import TokenBlacklist
from app.schemas.token_blacklist import TokenBlacklistCreate, TokenBlacklistResponse
from app.core.dependencies import require_role
from app.models.usuario import Usuario
from typing import List
from datetime import datetime

router = APIRouter(prefix="/token-blacklist", tags=["Token Blacklist"])

@router.post("/", response_model=TokenBlacklistResponse, status_code=status.HTTP_201_CREATED)
def add_token_to_blacklist(token_data: TokenBlacklistCreate, db: Session = Depends(get_db), 
                           usuario_actual: Usuario = Depends(require_role(["admin"]))):
    """
    Agrega un token a la lista negra.
    Requiere rol de administrador.
    """
    # Verificar si el token ya está en la lista negra
    existe = db.query(TokenBlacklist).filter(TokenBlacklist.token == token_data.token).first()
    if existe:
        raise HTTPException(status_code=400, detail="El token ya está en la lista negra")
    
    db_token = TokenBlacklist(token=token_data.token)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

@router.get("/", response_model=List[TokenBlacklistResponse])
def get_blacklisted_tokens(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
                           usuario_actual: Usuario = Depends(require_role(["admin"]))):
    """
    Obtiene todos los tokens en la lista negra.
    Requiere rol de administrador.
    """
    tokens = db.query(TokenBlacklist).offset(skip).limit(limit).all()
    return tokens

@router.get("/{token_id}", response_model=TokenBlacklistResponse)
def get_blacklisted_token(token_id: int, db: Session = Depends(get_db), 
                         usuario_actual: Usuario = Depends(require_role(["admin"]))):
    """
    Obtiene un token específico de la lista negra por su ID.
    Requiere rol de administrador.
    """
    token = db.query(TokenBlacklist).filter(TokenBlacklist.id == token_id).first()
    if token is None:
        raise HTTPException(status_code=404, detail="Token no encontrado")
    return token

@router.delete("/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blacklisted_token(token_id: int, db: Session = Depends(get_db), 
                            usuario_actual: Usuario = Depends(require_role(["admin"]))):
    """
    Elimina un token de la lista negra por su ID.
    Requiere rol de administrador.
    """
    token = db.query(TokenBlacklist).filter(TokenBlacklist.id == token_id).first()
    if token is None:
        raise HTTPException(status_code=404, detail="Token no encontrado")
    db.delete(token)
    db.commit()
    return None

@router.get("/check/{token_string}", response_model=bool)
def check_if_blacklisted(token_string: str, db: Session = Depends(get_db), 
                        usuario_actual: Usuario = Depends(require_role(["admin"]))):
    """
    Verifica si un token está en la lista negra.
    Requiere rol de administrador.
    """
    token = db.query(TokenBlacklist).filter(TokenBlacklist.token == token_string).first()
    return token is not None

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_usuario(token_data: TokenBlacklistCreate, db: Session = Depends(get_db), 
                  usuario_actual: Usuario = Depends(require_role([]))):
    """
    Cierra la sesión del usuario actual agregando su token a la lista negra.
    Accesible para todos los usuarios autenticados.
    """
    # Verificar si el token ya está en la lista negra
    existe = db.query(TokenBlacklist).filter(TokenBlacklist.token == token_data.token).first()
    if existe:
        return None
    
    db_token = TokenBlacklist(token=token_data.token)
    db.add(db_token)
    db.commit()
    return None