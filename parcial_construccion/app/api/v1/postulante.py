from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.postulante import PostulanteCreate, PostulanteOut
from app.models.postulante import Postulante
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/postulante", tags=["Postulante"])

# Crear un postulante
@router.post("/", response_model=PostulanteOut)
def crear_postulante(postulante: PostulanteCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    nuevo_postulante = Postulante(
        usuario_id=postulante.usuario_id,
        nombre_completo=postulante.nombre_completo,
        fecha_nacimiento=postulante.fecha_nacimiento,
        telefono=postulante.telefono
    )
    db.add(nuevo_postulante)
    db.commit()
    db.refresh(nuevo_postulante)
    return nuevo_postulante

# Obtener todos los postulantes
@router.get("/", response_model=list[PostulanteOut])
def obtener_postulantes(db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    postulantes = db.query(Postulante).all()
    return postulantes

# Obtener un postulante por ID
@router.get("/{postulante_id}", response_model=PostulanteOut)
def obtener_postulante(postulante_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    postulante = db.query(Postulante).filter(Postulante.id == postulante_id).first()
    if not postulante:
        raise HTTPException(status_code=404, detail="Postulante no encontrado")
    return postulante

# Actualizar postulante
@router.put("/{postulante_id}", response_model=PostulanteOut)
def actualizar_postulante(postulante_id: int, datos: PostulanteCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    postulante = db.query(Postulante).filter(Postulante.id == postulante_id).first()
    if not postulante:
        raise HTTPException(status_code=404, detail="Postulante no encontrado")

    postulante.nombre_completo = datos.nombre_completo
    postulante.fecha_nacimiento = datos.fecha_nacimiento
    postulante.telefono = datos.telefono
    postulante.usuario_id = datos.usuario_id

    db.commit()
    db.refresh(postulante)
    return postulante

@router.delete("/{postulante_id}")
def eliminar_postulante(postulante_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    postulante = db.query(Postulante).filter(Postulante.id == postulante_id).first()
    if not postulante:
        raise HTTPException(status_code=404, detail="Postulante no encontrado")

    db.delete(postulante)
    db.commit()
    
    # Confirmación de eliminación
    return {"detail": "Postulante eliminado exitosamente"}