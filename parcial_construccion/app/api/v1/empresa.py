from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.empresa import EmpresaCreate, EmpresaOut
from app.models.empresa import Empresa
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/empresa", tags=["Empresa"])

@router.post("/", response_model=EmpresaOut)
def crear_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    nueva_empresa = Empresa(
        nombre=empresa.nombre,
        direccion=empresa.direccion,
        telefono=empresa.telefono,
        email=empresa.email
    )
    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)
    return nueva_empresa

@router.get("/", response_model=list[EmpresaOut])
def obtener_empresas(db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    empresas = db.query(Empresa).all()
    return empresas

@router.get("/{empresa_id}", response_model=EmpresaOut)
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa

@router.put("/{empresa_id}", response_model=EmpresaOut)
def actualizar_empresa(empresa_id: int, datos: EmpresaCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    empresa.nombre = datos.nombre
    empresa.direccion = datos.direccion
    empresa.telefono = datos.telefono
    empresa.email = datos.email

    db.commit()
    db.refresh(empresa)
    return empresa

@router.delete("/{empresa_id}", response_model=EmpresaOut)
def eliminar_empresa(empresa_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    db.delete(empresa)
    db.commit()
    return empresa
