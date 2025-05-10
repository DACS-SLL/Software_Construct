from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.notifica import crear_notificacion, obtener_notificaciones_por_usuario, marcar_como_leida
from app.schemas.notificaciones import NotificacionCreate, NotificacionOut
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])

# Crear notificación
@router.post("/", response_model=NotificacionOut)
def crear_notificacion_route(notificacion: NotificacionCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador"]))):
    nueva_notificacion = crear_notificacion(db, notificacion, usuario_id=notificacion.usuario_id)

    return nueva_notificacion

# Obtener notificaciones de un usuario
@router.get("/usuario/{usuario_id}", response_model=list[NotificacionOut])
def obtener_notificaciones_por_usuario_route(usuario_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    notificaciones = obtener_notificaciones_por_usuario(db, usuario_id)
    return notificaciones

# Marcar notificación como leída
@router.put("/leida/{notificacion_id}", response_model=NotificacionOut)
def marcar_como_leida_route(notificacion_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    notificacion = marcar_como_leida(db, notificacion_id)
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return notificacion
