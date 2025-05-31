from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal, engine, Base
from app.models import (
    Rol, Usuario, Empresa, Postulante, Categoria, OfertaLaboral, Postulacion, Curriculum,
    Educacion, ExperienciaLaboral, Entrevista, Habilidad, Notificacion, Mensaje,
    TokenBlacklist, Evaluacion, RegistroActividad
)
from datetime import datetime, date

def reset_and_seed():
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        # Desactivar FK (solo para SQLite)
        session.execute(text("PRAGMA foreign_keys = OFF;"))

        # Eliminar datos en orden dependiente (de hijos a padres)
        session.query(Evaluacion).delete()
        session.query(RegistroActividad).delete()
        session.query(Mensaje).delete()
        session.query(Notificacion).delete()
        session.query(Habilidad).delete()
        session.query(Entrevista).delete()
        session.query(ExperienciaLaboral).delete()
        session.query(Educacion).delete()
        session.query(Curriculum).delete()
        session.query(Postulacion).delete()
        session.query(OfertaLaboral).delete()
        session.query(Categoria).delete()
        session.query(Postulante).delete()
        session.query(Empresa).delete()
        session.query(Usuario).delete()
        session.query(Rol).delete()
        session.query(TokenBlacklist).delete()

        session.commit()
        session.execute(text("PRAGMA foreign_keys = ON;"))

        # --- Insertar datos de ejemplo ---

        # Roles
        admin_rol = Rol(nombre="Administrador")
        user_rol = Rol(nombre="Usuario")
        session.add_all([admin_rol, user_rol])
        session.commit()

        # Usuarios
        user1 = Usuario(
            nombre="Daniel Casas",
            email="daniel@example.com",
            contraseña_hash="hash123",
            rol=admin_rol,
            activo=True
        )
        user2 = Usuario(
            nombre="Juan Perez",
            email="juan@example.com",
            contraseña_hash="hash456",
            rol=user_rol,
            activo=True
        )
        session.add_all([user1, user2])
        session.commit()

        # Empresas
        empresa1 = Empresa(
            usuario=user1,
            nombre="Empresa XYZ",
            rubro="Tecnología",
            direccion="Av. Arequipa 123",
            descripcion="Empresa dedicada al desarrollo de software"
        )
        session.add(empresa1)
        session.commit()

        # Postulantes
        postulante1 = Postulante(
            usuario=user2,
            nombre_completo="Juan Perez",
            fecha_nacimiento=date(1995, 5, 10),
            telefono="987654321"
        )
        session.add(postulante1)
        session.commit()

        # Categorías
        categoria1 = Categoria(nombre="Desarrollo Web")
        categoria2 = Categoria(nombre="Marketing")
        session.add_all([categoria1, categoria2])
        session.commit()

        # Oferta Laboral
        oferta1 = OfertaLaboral(
            empresa=empresa1,
            titulo="Desarrollador Backend",
            descripcion="Se busca desarrollador con experiencia en Python y SQLAlchemy",
            ubicacion="Arequipa",
            fecha_publicacion=date.today(),
            categoria=categoria1,
            estado="activo"
        )
        session.add(oferta1)
        session.commit()

        # Postulación
        postulacion1 = Postulacion(
            postulante=postulante1,
            oferta=oferta1,
            fecha_postulacion=date.today(),
            estado="pendiente"
        )
        session.add(postulacion1)
        session.commit()

        # Curriculum
        curriculum1 = Curriculum(
            postulante=postulante1,
            ruta_archivo="curriculum_juan.pdf"
        )
        session.add(curriculum1)
        session.commit()

        # Educación
        educacion1 = Educacion(
            curriculum=curriculum1,
            institucion="Universidad Nacional de Arequipa",
            titulo="Ingeniería de Sistemas",
            fecha_inicio=date(2013, 3, 1),
            fecha_fin=date(2018, 12, 31)
        )
        session.add(educacion1)
        session.commit()

        # Experiencia Laboral
        experiencia1 = ExperienciaLaboral(
            curriculum=curriculum1,
            empresa="Empresa ABC",
            cargo="Programador Junior",
            descripcion="Desarrollo de aplicaciones web",
            fecha_inicio=date(2019, 1, 1),
            fecha_fin=date(2021, 6, 30)
        )
        session.add(experiencia1)
        session.commit()

        # Entrevista
        entrevista1 = Entrevista(
            postulacion=postulacion1,
            fecha=datetime.now(),
            modalidad="Virtual",
            resultado="Pendiente"
        )
        session.add(entrevista1)
        session.commit()

        # Habilidades
        habilidad1 = Habilidad(nombre="Python")
        habilidad2 = Habilidad(nombre="SQLAlchemy")
        session.add_all([habilidad1, habilidad2])
        session.commit()

        # Notificaciones
        notificacion1 = Notificacion(
            usuario=user1,
            mensaje="Bienvenido al sistema",
            leida=False
        )
        session.add(notificacion1)
        session.commit()

        # Mensajes
        mensaje1 = Mensaje(
            emisor=user1,
            receptor=user2,
            contenido="Hola Juan, bienvenido.",
        )
        session.add(mensaje1)
        session.commit()

        # TokenBlacklist (vacío de ejemplo)
        # Evaluaciones
        evaluacion1 = Evaluacion(
            postulacion=postulacion1,
            evaluador=user1,
            comentario="Buen candidato",
            puntaje=85
        )
        session.add(evaluacion1)
        session.commit()

        # Registro Actividad
        registro1 = RegistroActividad(
            usuario=user1,
            accion="Creación de usuario admin",
        )
        session.add(registro1)
        session.commit()

        print("Datos reiniciados y cargados correctamente.")

if __name__ == "__main__":
    reset_and_seed()
