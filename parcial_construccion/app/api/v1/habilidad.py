from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.habilidad import Habilidad
from app.schemas.habilidad import HabilidadCreate, HabilidadUpdate, HabilidadOut
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/habilidades", tags=["Habilidades"])

# Crear habilidad
@router.post("/", response_model=HabilidadOut)
def crear_habilidad(habilidad: HabilidadCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    nueva_habilidad = Habilidad(**habilidad.dict())
    db.add(nueva_habilidad)
    db.commit()
    db.refresh(nueva_habilidad)
    return nueva_habilidad

# Obtener todas las habilidades
@router.get("/", response_model=list[HabilidadOut])
def obtener_habilidades(db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "postulante", "empleador"]))):
    habilidades = db.query(Habilidad).all()
    return habilidades

# Obtener habilidad por ID
@router.get("/{habilidad_id}", response_model=HabilidadOut)
def obtener_habilidad(habilidad_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "postulante", "empleador"]))):
    habilidad = db.query(Habilidad).filter(Habilidad.id == habilidad_id).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")
    return habilidad

# Actualizar habilidad
@router.put("/{habilidad_id}", response_model=HabilidadOut)
def actualizar_habilidad(habilidad_id: int, habilidad: HabilidadUpdate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    habilidad_existente = db.query(Habilidad).filter(Habilidad.id == habilidad_id).first()
    if not habilidad_existente:
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")
    
    habilidad_existente.nombre = habilidad.nombre
    db.commit()
    db.refresh(habilidad_existente)
    return habilidad_existente

# Eliminar habilidad
@router.delete("/{habilidad_id}", response_model=HabilidadOut)
def eliminar_habilidad(habilidad_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    habilidad = db.query(Habilidad).filter(Habilidad.id == habilidad_id).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")

    db.delete(habilidad)
    db.commit()
    return habilidad
