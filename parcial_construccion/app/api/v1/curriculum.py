from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.curriculum import Curriculum
from app.schemas.curriculum import CurriculumCreate, CurriculumUpdate, CurriculumOut
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/curriculum", tags=["Curriculum"])

# Crear curriculum
@router.post("/", response_model=CurriculumOut)
def crear_curriculum(curriculum: CurriculumCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "postulante"]))):
    nuevo_curriculum = Curriculum(
        postulante_id=curriculum.postulante_id,
        ruta_archivo=curriculum.ruta_archivo,
        fecha_subida=curriculum.fecha_subida,
    )
    db.add(nuevo_curriculum)
    db.commit()
    db.refresh(nuevo_curriculum)
    return nuevo_curriculum

# Obtener todos los curriculums
@router.get("/", response_model=list[CurriculumOut])
def obtener_curriculums(db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador"]))):
    curriculums = db.query(Curriculum).all()
    return curriculums

# Obtener curriculum por ID
@router.get("/{curriculum_id}", response_model=CurriculumOut)
def obtener_curriculum(curriculum_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    curriculum = db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum no encontrado")
    return curriculum

# Actualizar curriculum
@router.put("/{curriculum_id}", response_model=CurriculumOut)
def actualizar_curriculum(curriculum_id: int, curriculum: CurriculumUpdate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin, postulante"]))):
    curriculum_existente = db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()
    if not curriculum_existente:
        raise HTTPException(status_code=404, detail="Curriculum no encontrado")

    curriculum_existente.postulante_id = curriculum.postulante_id
    curriculum_existente.ruta_archivo = curriculum.ruta_archivo
    curriculum_existente.fecha_subida = curriculum.fecha_subida

    db.commit()
    db.refresh(curriculum_existente)
    return curriculum_existente

# Eliminar curriculum
@router.delete("/{curriculum_id}", response_model=CurriculumOut)
def eliminar_curriculum(curriculum_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "postulante"]))):
    curriculum = db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum no encontrado")

    db.delete(curriculum)
    db.commit()
    return curriculum

# Obtener curriculum por postulante
@router.get("/postulante/{postulante_id}", response_model=list[CurriculumOut])
def obtener_curriculum_por_postulante(postulante_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    curriculums = db.query(Curriculum).filter(Curriculum.postulante_id == postulante_id).all()
    return curriculums