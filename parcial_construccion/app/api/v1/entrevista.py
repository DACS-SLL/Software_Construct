from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.entrevista import Entrevista
from app.schemas.entrevista import EntrevistaCreate, EntrevistaUpdate, EntrevistaOut
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/entrevista", tags=["Entrevistas"])

# Crear entrevista
@router.post("/", response_model=EntrevistaOut)
def crear_entrevista(entrevista: EntrevistaCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador"]))):
    nueva_entrevista = Entrevista(**entrevista.dict())
    db.add(nueva_entrevista)
    db.commit()
    db.refresh(nueva_entrevista)
    return nueva_entrevista

# Obtener todas las entrevistas
@router.get("/", response_model=list[EntrevistaOut])
def obtener_entrevistas(db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    entrevistas = db.query(Entrevista).all()
    return entrevistas

# Obtener entrevista por ID
@router.get("/{entrevista_id}", response_model=EntrevistaOut)
def obtener_entrevista(entrevista_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    entrevista = db.query(Entrevista).filter(Entrevista.id == entrevista_id).first()
    if not entrevista:
        raise HTTPException(status_code=404, detail="Entrevista no encontrada")
    return entrevista

# Actualizar entrevista
@router.put("/{entrevista_id}", response_model=EntrevistaOut)
def actualizar_entrevista(entrevista_id: int, entrevista: EntrevistaUpdate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador"]))):
    entrevista_existente = db.query(Entrevista).filter(Entrevista.id == entrevista_id).first()
    if not entrevista_existente:
        raise HTTPException(status_code=404, detail="Entrevista no encontrada")
    
    for campo, valor in entrevista.dict().items():
        setattr(entrevista_existente, campo, valor)

    db.commit()
    db.refresh(entrevista_existente)
    return entrevista_existente

# Eliminar entrevista
@router.delete("/{entrevista_id}", response_model=EntrevistaOut)
def eliminar_entrevista(entrevista_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador"]))):
    entrevista = db.query(Entrevista).filter(Entrevista.id == entrevista_id).first()
    if not entrevista:
        raise HTTPException(status_code=404, detail="Entrevista no encontrada")

    db.delete(entrevista)
    db.commit()
    return entrevista

# Obtener entrevistas por postulación
@router.get("/postulacion/{postulacion_id}", response_model=list[EntrevistaOut])
def obtener_entrevistas_por_postulacion(postulacion_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleador", "postulante"]))):
    entrevistas = db.query(Entrevista).filter(Entrevista.postulacion_id == postulacion_id).all()
    return entrevistas
