# 📦 Plataforma de Empleo – Módulo Base de Datos

**Parte desarrollada por el DB Manager** del proyecto de construcción de una **plataforma web de gestión de ofertas y solicitudes de empleo**.

Incluye:
- Modelado completo de la base de datos (17 entidades)
- Estructura con SQLAlchemy
- Migraciones con Alembic
- Conexión a PostgreSQL 

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

### 1. Clonar el repositorio

- git clone https://github.com/DACS-SLL/Software_Construct.git
- cd Sofware_Construct/parcial_construccion


### 2. Crear entorno virtual e instalar dependencias
   
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt


### 3. Crear base de datos en PostgreSQL

Nombre: db_parcial_construccion
Usuario: postgres
Contraseña: admin (o de acuerdo a su configuración de su postgres se le cambia)


Asegúrate de editar los siguientes archivos con tu usuario y contraseña de PostgreSQL:

- app/database.py
- alembic.ini

Ejemplo de cadena de conexión:
postgresql://miusuario:admin@localhost/db_parcial_construccion
(cambiar de acuerdo a su postgres)

### 4. Aplicar migraciones

alembic upgrade head

- Esto creará automáticamente todas las tablas en tu base de datos PostgreSQL.

📁 Estructura del Proyecto

parcial_construccion/
├── app/
│   ├── models/
│   │   └── models.py        # Todos los modelos definidos aquí
│   └── database.py          # Conexión a PostgreSQL
├── alembic/
│   ├── env.py               # Configuración Alembic
│   └── versions/            # Migraciones autogeneradas
├── alembic.ini              # Cadena de conexión y configuración general
├── requirements.txt         # Dependencias
└── README.md              

