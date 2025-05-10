from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaOut
from app.database import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/categorias", tags=["Categorias"])

# Crear categoria
@router.post("/", response_model=CategoriaOut)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    nueva_categoria = Categoria(nombre=categoria.nombre)
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

# Obtener todas las categorias
@router.get("/", response_model=list[CategoriaOut])
def obtener_categorias(db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleado"]))):
    categorias = db.query(Categoria).all()
    return categorias

# Obtener categoria por ID
@router.get("/{categoria_id}", response_model=CategoriaOut)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin", "empleado"]))):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria

# Actualizar categoria
@router.put("/{categoria_id}", response_model=CategoriaOut)
def actualizar_categoria(categoria_id: int, categoria: CategoriaUpdate, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    categoria_existente = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria_existente:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    categoria_existente.nombre = categoria.nombre

    db.commit()
    db.refresh(categoria_existente)
    return categoria_existente

# Eliminar categoria
@router.delete("/{categoria_id}", response_model=CategoriaOut)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db), usuario_actual: str = Depends(require_role(["admin"]))):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    db.delete(categoria)
    db.commit()
    return categoria
