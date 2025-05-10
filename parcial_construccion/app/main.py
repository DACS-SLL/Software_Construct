### main.py
from fastapi import FastAPI
from app.api.v1 import empresa, auth, postulante, oferta_laboral, categoria, postulacion  # Rutas ejemplo
from app.database import engine, Base

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobHub API", version="1.0.0")

app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(empresa.router, prefix="/api/v1", tags=["Empresas"])
app.include_router(postulante.router, prefix="/api/v1", tags=["Postulantes"])
app.include_router(categoria.router, prefix="/api/v1", tags=["Categorías"])
app.include_router(oferta_laboral.router, prefix="/api/v1", tags=["Ofertas Laborales"])
app.include_router(postulacion.router, prefix="/api/v1", tags=["Postulaciones"])
# Incluir rutas
#app.include_router(usuario.router, prefix="/api/v1/usuarios", tags=["Usuarios"])
#app.include_router(oferta.router, prefix="/api/v1/ofertas", tags=["Ofertas"])