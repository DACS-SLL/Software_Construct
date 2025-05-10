from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.oferta_laboral import OfertaLaboral
from app.schemas.oferta_laboral import OfertaLaboralCreate, OfertaLaboralUpdate, OfertaLaboralOut
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/ofertas", tags=["Ofertas Laborales"])

# Crear oferta laboral
@router.post("/", response_model=OfertaLaboralOut)
def crear_oferta(oferta: OfertaLaboralCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    nueva_oferta = OfertaLaboral(
        titulo=oferta.titulo,
        descripcion=oferta.descripcion,
        ubicacion=oferta.ubicacion,
        fecha_publicacion=oferta.fecha_publicacion,
        estado=oferta.estado,
        categoria_id=oferta.categoria_id,
        empresa_id=oferta.empresa_id,
    )
    db.add(nueva_oferta)
    db.commit()
    db.refresh(nueva_oferta)
    return nueva_oferta

# Obtener todas las ofertas laborales
@router.get("/", response_model=list[OfertaLaboralOut])
def obtener_ofertas(db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleado"]))):
    ofertas = db.query(OfertaLaboral).all()
    return ofertas

# Obtener oferta laboral por ID
@router.get("/{oferta_id}", response_model=OfertaLaboralOut)
def obtener_oferta(oferta_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleado"]))):
    oferta = db.query(OfertaLaboral).filter(OfertaLaboral.id == oferta_id).first()
    if not oferta:
        raise HTTPException(status_code=404, detail="Oferta laboral no encontrada")
    return oferta

# Actualizar oferta laboral
@router.put("/{oferta_id}", response_model=OfertaLaboralOut)
def actualizar_oferta(oferta_id: int, oferta: OfertaLaboralUpdate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    oferta_existente = db.query(OfertaLaboral).filter(OfertaLaboral.id == oferta_id).first()
    if not oferta_existente:
        raise HTTPException(status_code=404, detail="Oferta laboral no encontrada")

    oferta_existente.titulo = oferta.titulo
    oferta_existente.descripcion = oferta.descripcion
    oferta_existente.ubicacion = oferta.ubicacion
    oferta_existente.fecha_publicacion = oferta.fecha_publicacion
    oferta_existente.estado = oferta.estado
    oferta_existente.categoria_id = oferta.categoria_id
    oferta_existente.empresa_id = oferta.empresa_id

    db.commit()
    db.refresh(oferta_existente)
    return oferta_existente

# Eliminar oferta laboral
@router.delete("/{oferta_id}", response_model=OfertaLaboralOut)
def eliminar_oferta(oferta_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    oferta = db.query(OfertaLaboral).filter(OfertaLaboral.id == oferta_id).first()
    if not oferta:
        raise HTTPException(status_code=404, detail="Oferta laboral no encontrada")

    db.delete(oferta)
    db.commit()
    return oferta
