from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.mensaje import crear_mensaje, obtener_mensajes_por_usuario, obtener_mensajes_por_emisor, obtener_mensajes_por_receptor
from app.schemas.mensaje import MensajeCreate, MensajeOut
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/mensajes", tags=["Mensajes"])

# Crear mensaje
@router.post("/", response_model=MensajeOut)
def crear_mensaje_route(mensaje: MensajeCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    nuevo_mensaje = crear_mensaje(db, mensaje.emisor_id, mensaje.receptor_id, mensaje.contenido)
    return nuevo_mensaje

# Obtener mensajes por usuario (emisor o receptor)
@router.get("/usuario/{usuario_id}", response_model=list[MensajeOut])
def obtener_mensajes_por_usuario_route(usuario_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    mensajes = obtener_mensajes_por_usuario(db, usuario_id)
    return mensajes

# Obtener mensajes enviados por un emisor
@router.get("/emisor/{emisor_id}", response_model=list[MensajeOut])
def obtener_mensajes_por_emisor_route(emisor_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    mensajes = obtener_mensajes_por_emisor(db, emisor_id)
    return mensajes

# Obtener mensajes recibidos por un receptor
@router.get("/receptor/{receptor_id}", response_model=list[MensajeOut])
def obtener_mensajes_por_receptor_route(receptor_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    mensajes = obtener_mensajes_por_receptor(db, receptor_id)
    return mensajes
