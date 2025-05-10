from datetime import datetime
from sqlalchemy.orm import Session
from app.models.mensaje import Mensaje
from app.schemas.mensaje import MensajeCreate

def crear_mensaje(db: Session, emisor_id: int, receptor_id: int, contenido: str):
    # Crear el mensaje
    mensaje = Mensaje(
        emisor_id=emisor_id,
        receptor_id=receptor_id,
        contenido=contenido,
        fecha_envio=datetime.utcnow()
    )
    
    # Guardar en la base de datos
    db.add(mensaje)
    db.commit()
    db.refresh(mensaje)
    
    return mensaje

def obtener_mensajes_por_usuario(db: Session, usuario_id: int):
    # Obtener los mensajes enviados o recibidos por el usuario
    return db.query(Mensaje).filter(
        (Mensaje.emisor_id == usuario_id) | (Mensaje.receptor_id == usuario_id)
    ).all()

def obtener_mensajes_por_receptor(db: Session, receptor_id: int):
    # Obtener mensajes de un receptor específico
    return db.query(Mensaje).filter(Mensaje.receptor_id == receptor_id).all()

def obtener_mensajes_por_emisor(db: Session, emisor_id: int):
    # Obtener mensajes de un emisor específico
    return db.query(Mensaje).filter(Mensaje.emisor_id == emisor_id).all()
