from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Directorio actual del proyecto
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# URL de la base de datos SQLite
#DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db_parcial_construccion.db')}"

DATABASE_URL = "postgresql://postgres:admin@localhost:5433/costrucción_db"

# Motor y sesión
#engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base para modelos
Base = declarative_base()