### main.py
from fastapi import FastAPI
from app.api.v1 import empresa, auth, postulante, oferta_laboral, categoria, postulacion, curriculum, educacion, experiencia_laboral, entrevista, mensaje, notificaciones, token_blacklist   # Rutas ejemplo
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
app.include_router(educacion.router, prefix="/api/v1", tags=["Educación"])
app.include_router(curriculum.router, prefix="/api/v1", tags=["Currículums"])
app.include_router(experiencia_laboral.router, prefix="/api/v1", tags=["Experiencia Laboral"])
app.include_router(entrevista.router, prefix="/api/v1", tags=["Entrevistas"])
app.include_router(mensaje.router, prefix="/api/v1", tags=["Mensajes"])
app.include_router(notificaciones.router, prefix="/api/v1", tags=["Notificaciones"])
app.include_router(token_blacklist.router, prefix="/api/v1", tags=["Token Blacklist"])

# Incluir rutas
