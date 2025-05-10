### main.py
from fastapi import FastAPI
from app.api.v1 import usuario, empresa, oferta  # Rutas ejemplo
from app.database import engine, Base

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobHub API", version="1.0.0")

# Incluir rutas
app.include_router(usuario.router, prefix="/api/v1/usuarios", tags=["Usuarios"])
app.include_router(empresa.router, prefix="/api/v1/empresas", tags=["Empresas"])
app.include_router(oferta.router, prefix="/api/v1/ofertas", tags=["Ofertas"])