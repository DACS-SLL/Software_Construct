from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.postulacion import Postulacion
from app.schemas.postulacion import PostulacionCreate, PostulacionUpdate, PostulacionOut
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/postulaciones", tags=["Postulaciones"])

# Crear postulación
@router.post("/", response_model=PostulacionOut)
def crear_postulacion(postulacion: PostulacionCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    nueva_postulacion = Postulacion(
        postulante_id=postulacion.postulante_id,
        oferta_id=postulacion.oferta_id,
        fecha_postulacion=postulacion.fecha_postulacion,
        estado=postulacion.estado
    )
    db.add(nueva_postulacion)
    db.commit()
    db.refresh(nueva_postulacion)
    return nueva_postulacion

# Obtener todas las postulaciones
@router.get("/", response_model=list[PostulacionOut])
def obtener_postulaciones(db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    postulaciones = db.query(Postulacion).all()
    return postulaciones

# Obtener postulación por ID
@router.get("/{postulacion_id}", response_model=PostulacionOut)
def obtener_postulacion(postulacion_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    postulacion = db.query(Postulacion).filter(Postulacion.id == postulacion_id).first()
    if not postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    return postulacion

# Actualizar postulación
@router.put("/{postulacion_id}", response_model=PostulacionOut)
def actualizar_postulacion(postulacion_id: int, postulacion: PostulacionUpdate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador"]))):
    postulacion_existente = db.query(Postulacion).filter(Postulacion.id == postulacion_id).first()
    if not postulacion_existente:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")

    postulacion_existente.postulante_id = postulacion.postulante_id
    postulacion_existente.oferta_id = postulacion.oferta_id
    postulacion_existente.fecha_postulacion = postulacion.fecha_postulacion
    postulacion_existente.estado = postulacion.estado

    db.commit()
    db.refresh(postulacion_existente)
    return postulacion_existente

# Eliminar postulación
@router.delete("/{postulacion_id}", response_model=PostulacionOut)
def eliminar_postulacion(postulacion_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "postulante"]))):
    postulacion = db.query(Postulacion).filter(Postulacion.id == postulacion_id).first()
    if not postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")

    db.delete(postulacion)
    db.commit()
    return postulacion

# Obtener postulaciones por postulante
@router.get("/postulante/{postulante_id}", response_model=list[PostulacionOut])
def obtener_postulaciones_por_postulante(postulante_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "postulante"]))):
    postulaciones = db.query(Postulacion).filter(Postulacion.postulante_id == postulante_id).all()
    return postulaciones

# Obtener postulaciones por oferta
@router.get("/oferta/{oferta_id}", response_model=list[PostulacionOut])
def obtener_postulaciones_por_oferta(oferta_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador"]))):
    postulaciones = db.query(Postulacion).filter(Postulacion.oferta_id == oferta_id).all()
    return postulaciones