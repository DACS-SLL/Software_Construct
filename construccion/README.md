# 📦 Plataforma de Empleo – API CRUD Completa

**Proyecto completo** de construcción de una **plataforma web de gestión de ofertas y solicitudes de empleo**.

Incluye:
- Modelado completo de la base de datos (17 entidades)
- API RESTful con FastAPI
- CRUD completo para todas las entidades
- Estructura con SQLAlchemy
- Base de datos SQLite para desarrollo

---

## 🧱 Estructura de la Base de Datos

Se diseñaron e implementaron las siguientes entidades principales:

1. Usuario  
2. Rol  
3. Empresa  
4. Postulante  
5. Oferta Laboral  
6. Postulación  
7. Curriculum  
8. Educación  
9. Experiencia Laboral  
10. Entrevista  
11. Habilidad  
12. Categoría  
13. Notificación  
14. Mensaje  
15. Token Blacklist  
16. Evaluación  
17. Registro de Actividad  

Todas las relaciones y claves foráneas están implementadas con SQLAlchemy.

---

## ⚙️ Instalación y Configuración

### 1. Requisitos previos

- Python 3.12.6 o superior
- Conocimientos básicos de APIs REST

### 2. Clonar el repositorio

```bash
git clone https://github.com/DACS-SLL/Software_Construct.git
cd Software_Construct/parcial_construccion
```

### 3. Crear entorno virtual e instalar dependencias
   
```bash
python -m venv venv
venv\Scripts\activate    # En Windows
source venv/bin/activate # En Linux/Mac
pip install -r requirements.txt
```

### 4. Base de datos

El proyecto utiliza SQLite para desarrollo, lo que facilita la configuración inicial:

- No requiere instalación de servidor de base de datos
- Se crea automáticamente al iniciar la aplicación
- Ideal para desarrollo y pruebas

Si prefieres usar PostgreSQL en producción, edita los siguientes archivos:

- `app/database.py`: Cambia la URL de conexión
- `alembic.ini`: Actualiza la configuración

### 5. Ejecutar la aplicación

```bash
python main.py
```

La API estará disponible en: http://localhost:8000

### 6. Explorar la API

Accede a la documentación interactiva en:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## 🧩 Endpoints de la API

La API implementa CRUD completo (Create, Read, Update, Delete) para todas las entidades:

- `/roles/` - Administración de roles
- `/usuarios/` - Gestión de usuarios
- `/empresas/` - Empresas registradas
- `/postulantes/` - Perfiles de postulantes
- `/categorias/` - Categorías de empleos
- `/ofertas-laborales/` - Ofertas de trabajo
- `/postulaciones/` - Aplicaciones a ofertas
- `/curriculums/` - Currículums de postulantes
- `/educaciones/` - Formación académica
- `/experiencias-laborales/` - Experiencia profesional
- `/entrevistas/` - Gestión de entrevistas
- `/habilidades/` - Habilidades y competencias
- `/notificaciones/` - Sistema de notificaciones
- `/mensajes/` - Comunicación entre usuarios
- `/token-blacklist/` - Seguridad para tokens JWT
- `/evaluaciones/` - Evaluaciones de postulantes
- `/registros-actividad/` - Registro de actividades

También incluye endpoints relacionales que facilitan consultas complejas:

- `/empresas/{empresa_id}/ofertas-laborales/` - Ofertas por empresa
- `/postulantes/{postulante_id}/postulaciones/` - Postulaciones por postulante
- `/ofertas-laborales/{oferta_id}/postulantes/` - Postulantes por oferta

## 📋 Guía de pruebas con Postman

Se incluye un archivo `probar_postman.md` con una guía paso a paso para probar todos los endpoints usando Postman. La guía incluye:

1. Creación de recursos básicos (roles, usuarios, empresas)
2. Gestión de ofertas laborales y postulaciones
3. Ejemplos de consultas relacionales
4. Actualizaciones y eliminaciones

## 📁 Estructura del Proyecto

```
parcial_construccion/
├── app/
│   ├── models/
│   │   └── models.py        # Todos los modelos definidos aquí
│   └── database.py          # Configuración de la base de datos
├── alembic/
│   ├── env.py               # Configuración Alembic
│   └── versions/            # Migraciones
├── main.py                  # API FastAPI y endpoints
├── alembic.ini              # Configuración general
├── probar_postman.md        # Guía para pruebas en Postman
├── requirements.txt         # Dependencias
└── README.md                # Documentación
```

## 🚀 Características Adicionales

- **Documentación automática**: Todas las rutas API están documentadas
- **Validación de datos**: Usando Pydantic para garantizar integridad
- **Endpoints relacionales**: Para consultas más complejas
- **Filtros parametrizados**: Búsqueda avanzada

## 📚 Tecnologías Utilizadas

- **Python 3.12.6**: Lenguaje de programación
- **FastAPI**: Framework web moderno y de alto rendimiento
- **SQLAlchemy**: ORM para interactuar con la base de datos
- **Pydantic**: Validación de datos y serialización
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación
- **SQLite**: Base de datos para desarrollo