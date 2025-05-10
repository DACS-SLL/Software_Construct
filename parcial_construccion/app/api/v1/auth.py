from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import LoginInput, Token, UsuarioCreate, UsuarioOut
from app.models.usuario import Usuario, Rol
from app.core.security import hash_password
from app.database import get_db
from app.core.dependencies import require_role
from app.core import security

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UsuarioOut)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    rol = db.query(Rol).filter(Rol.id == usuario.rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no válido")

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        contraseña_hash=hash_password(usuario.password),
        rol_id=usuario.rol_id,
        activo=True
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post("/login", response_model=Token)
def login_usuario(login: LoginInput, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == login.email).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not usuario.activo:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    if not security.verify_password(login.password, usuario.contraseña_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = security.create_access_token(data={"sub": usuario.email, "rol": usuario.rol.nombre})
    return {"access_token": token, "token_type": "bearer"}

@router.put("/edit/{user_id}", response_model=UsuarioOut)
def editar_usuario(user_id: int, datos: UsuarioCreate, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(require_role(["admin"]))):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = datos.nombre
    usuario.email = datos.email
    usuario.rol_id = datos.rol_id
    usuario.contraseña_hash = hash_password(datos.password)
    
    db.commit()
    db.refresh(usuario)
    return usuario



@router.delete("/delete/{user_id}", response_model=UsuarioOut)
def eliminar_usuario(user_id: int, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(require_role(["admin"]))):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return usuario


@router.get("/all", response_model=list[UsuarioOut])
def obtener_usuarios(db: Session = Depends(get_db), usuario_actual: Usuario = Depends(require_role(["admin"]))):
    usuarios = db.query(Usuario).all()
    return usuarios
