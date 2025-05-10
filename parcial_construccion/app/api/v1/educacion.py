from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.educacion import Educacion
from app.schemas.educacion import EducacionCreate, EducacionUpdate, EducacionOut
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/educacion", tags=["Educación"])

# Crear registro de educación
@router.post("/", response_model=EducacionOut)
def crear_educacion(educacion: EducacionCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["postulante"]))):
    nueva_educacion = Educacion(
        curriculum_id=educacion.curriculum_id,
        institucion=educacion.institucion,
        titulo=educacion.titulo,
        fecha_inicio=educacion.fecha_inicio,
        fecha_fin=educacion.fecha_fin,
    )
    db.add(nueva_educacion)
    db.commit()
    db.refresh(nueva_educacion)
    return nueva_educacion

# Obtener todos los registros de educación
@router.get("/", response_model=list[EducacionOut])
def obtener_educaciones(db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    educaciones = db.query(Educacion).all()
    return educaciones

# Obtener registro de educación por ID
@router.get("/{educacion_id}", response_model=EducacionOut)
def obtener_educacion(educacion_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    educacion = db.query(Educacion).filter(Educacion.id == educacion_id).first()
    if not educacion:
        raise HTTPException(status_code=404, detail="Registro de educación no encontrado")
    return educacion

# Actualizar registro de educación
@router.put("/{educacion_id}", response_model=EducacionOut)
def actualizar_educacion(educacion_id: int, educacion: EducacionUpdate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["postulante"]))):
    educacion_existente = db.query(Educacion).filter(Educacion.id == educacion_id).first()
    if not educacion_existente:
        raise HTTPException(status_code=404, detail="Registro de educación no encontrado")

    educacion_existente.curriculum_id = educacion.curriculum_id
    educacion_existente.institucion = educacion.institucion
    educacion_existente.titulo = educacion.titulo
    educacion_existente.fecha_inicio = educacion.fecha_inicio
    educacion_existente.fecha_fin = educacion.fecha_fin

    db.commit()
    db.refresh(educacion_existente)
    return educacion_existente

# Eliminar registro de educación
@router.delete("/{educacion_id}", response_model=EducacionOut)
def eliminar_educacion(educacion_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "postulante"]))):
    educacion = db.query(Educacion).filter(Educacion.id == educacion_id).first()
    if not educacion:
        raise HTTPException(status_code=404, detail="Registro de educación no encontrado")

    db.delete(educacion)
    db.commit()
    return educacion

# Obtener educación por curriculum
@router.get("/curriculum/{curriculum_id}", response_model=list[EducacionOut])
def obtener_educacion_por_curriculum(curriculum_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    educaciones = db.query(Educacion).filter(Educacion.curriculum_id == curriculum_id).all()
    return educaciones