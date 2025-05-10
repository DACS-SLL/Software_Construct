from sqlalchemy.orm import Session
from app.models.notificacion import Notificacion
from app.schemas.notificaciones import NotificacionCreate
from datetime import datetime

def crear_notificacion(db: Session, notificacion: NotificacionCreate, usuario_id: int):
    nueva = Notificacion(
        mensaje=notificacion.mensaje,
        leida=False,
        fecha_envio=datetime.utcnow(),
        usuario_id=usuario_id
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_notificaciones_por_usuario(db: Session, usuario_id: int):
    return db.query(Notificacion).filter(Notificacion.usuario_id == usuario_id).order_by(Notificacion.fecha_envio.desc()).all()

def marcar_como_leida(db: Session, notificacion_id: int):
    notificacion = db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()
    if notificacion:
        notificacion.leida = True
        db.commit()
    return notificacion
