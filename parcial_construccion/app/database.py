from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# ------
# Cambia estos datos a los de tu PostgreSQL local
DATABASE_URL = "postgresql://postgres:admin@localhost/db_parcial_construccion"
#------

# Motor y sesión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base para modelos
Base = declarative_base()
