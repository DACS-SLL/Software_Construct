from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import (
    Rol, Usuario, Empresa, Postulante, Categoria, OfertaLaboral,
    Postulacion, Curriculum, Educacion, ExperienciaLaboral, Entrevista,
    Habilidad, Notificacion, Mensaje, TokenBlacklist, Evaluacion, RegistroActividad
)
from app.database import Base, engine as postgres_engine, SessionLocal

# ✅ Conexión a SQLite (con check_same_thread solo aquí)
sqlite_engine = create_engine("sqlite:///./app/db_parcial_construccion.db", connect_args={"check_same_thread": False})
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()

# ✅ Sesión PostgreSQL (ya sin check_same_thread)
postgres_session = SessionLocal()

# Crear las tablas en PostgreSQL si aún no existen
Base.metadata.create_all(bind=postgres_engine)

# Función genérica para migrar modelos
def migrar_tabla(modelo):
    print(f"🔄 Migrando: {modelo.__tablename__}")
    registros = sqlite_session.query(modelo).all()
    for registro in registros:
        postgres_session.merge(registro)  # Evita conflictos con PK existentes
    postgres_session.commit()

# Lista de modelos en orden correcto por relaciones
modelos_ordenados = [
    Rol,
    Usuario,
    Empresa,
    Postulante,
    Categoria,
    OfertaLaboral,
    Postulacion,
    Curriculum,
    Educacion,
    ExperienciaLaboral,
    Entrevista,
    Habilidad,
    Notificacion,
    Mensaje,
    TokenBlacklist,
    Evaluacion,
    RegistroActividad
]

# Ejecutar migración
for modelo in modelos_ordenados:
    migrar_tabla(modelo)

# Cerrar sesiones
sqlite_session.close()
postgres_session.close()

print("✅ Migración completada sin errores.")
