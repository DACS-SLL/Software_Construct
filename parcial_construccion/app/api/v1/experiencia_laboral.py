from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.experiencia_laboral import ExperienciaLaboral
from app.schemas.experiencia_laboral import ExperienciaLaboralCreate, ExperienciaLaboralUpdate, ExperienciaLaboralOut
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/experiencia-laboral", tags=["Experiencia Laboral"])

# Crear experiencia laboral
@router.post("/", response_model=ExperienciaLaboralOut)
def crear_experiencia_laboral(experiencia: ExperienciaLaboralCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["postulante"]))):
    nueva_experiencia = ExperienciaLaboral(
        curriculum_id=experiencia.curriculum_id,
        empresa=experiencia.empresa,
        cargo=experiencia.cargo,
        descripcion=experiencia.descripcion,
        fecha_inicio=experiencia.fecha_inicio,
        fecha_fin=experiencia.fecha_fin,
    )
    db.add(nueva_experiencia)
    db.commit()
    db.refresh(nueva_experiencia)
    return nueva_experiencia

# Obtener todas las experiencias laborales
@router.get("/", response_model=list[ExperienciaLaboralOut])
def obtener_experiencias_laborales(db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    experiencias = db.query(ExperienciaLaboral).all()
    return experiencias

# Obtener experiencia laboral por ID
@router.get("/{experiencia_id}", response_model=ExperienciaLaboralOut)
def obtener_experiencia_laboral(experiencia_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    experiencia = db.query(ExperienciaLaboral).filter(ExperienciaLaboral.id == experiencia_id).first()
    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiencia laboral no encontrada")
    return experiencia

# Actualizar experiencia laboral
@router.put("/{experiencia_id}", response_model=ExperienciaLaboralOut)
def actualizar_experiencia_laboral(experiencia_id: int, experiencia: ExperienciaLaboralUpdate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["postulante"]))):
    experiencia_existente = db.query(ExperienciaLaboral).filter(ExperienciaLaboral.id == experiencia_id).first()
    if not experiencia_existente:
        raise HTTPException(status_code=404, detail="Experiencia laboral no encontrada")

    experiencia_existente.curriculum_id = experiencia.curriculum_id
    experiencia_existente.empresa = experiencia.empresa
    experiencia_existente.cargo = experiencia.cargo
    experiencia_existente.descripcion = experiencia.descripcion
    experiencia_existente.fecha_inicio = experiencia.fecha_inicio
    experiencia_existente.fecha_fin = experiencia.fecha_fin

    db.commit()
    db.refresh(experiencia_existente)
    return experiencia_existente

# Eliminar experiencia laboral
@router.delete("/{experiencia_id}", response_model=ExperienciaLaboralOut)
def eliminar_experiencia_laboral(experiencia_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "postulante"]))):
    experiencia = db.query(ExperienciaLaboral).filter(ExperienciaLaboral.id == experiencia_id).first()
    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiencia laboral no encontrada")

    db.delete(experiencia)
    db.commit()
    return experiencia

# Obtener experiencias laborales por curriculum
@router.get("/curriculum/{curriculum_id}", response_model=list[ExperienciaLaboralOut])
def obtener_experiencias_por_curriculum(curriculum_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    experiencias = db.query(ExperienciaLaboral).filter(ExperienciaLaboral.curriculum_id == curriculum_id).all()
    return experiencias