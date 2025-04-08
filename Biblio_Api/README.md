# API de Gestión de Biblioteca

## Descripción
Esta es una API RESTful mejorada para gestionar autores, libros y géneros de una biblioteca. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre las entidades, establece relaciones entre ellas e implementa autenticación y autorización con JWT.

## Características principales
- Autenticación y autorización con tokens JWT
- Gestión completa de autores (crear, obtener, actualizar, eliminar lógico)
- Gestión completa de libros (crear, obtener, actualizar, eliminar lógico)
- Gestión de géneros literarios
- Relación muchos a muchos entre autores y libros (un libro puede tener varios autores y un autor puede escribir varios libros)
- Relación muchos a muchos entre libros y géneros
- Borrado lógico (soft delete) en lugar de eliminación física de registros
- Validación de datos de entrada con Marshmallow
- Manejo de errores HTTP detallado
- Búsqueda avanzada de libros por título, autor o género
- Implementación con blueprints para organizar el código
- Configuración segura mediante variables de entorno

## Tecnologías utilizadas
- Flask: Framework web en Python
- SQLAlchemy: ORM para la base de datos
- Flask-Migrate: Migraciones de base de datos
- Flask-JWT-Extended: Autenticación y autorización con tokens JWT
- Marshmallow: Validación de esquemas
- SQLite: Base de datos (para desarrollo, configurable para otras bases de datos en producción)
- Python-dotenv: Gestión de variables de entorno

## Estructura del proyecto
```
biblioteca_api/
│
├── app.py                # Archivo principal de la aplicación
├── config.py             # Configuraciones de la aplicación
├── .env                  # Variables de entorno (no incluido en el repositorio)
├── .env.example          # Ejemplo de archivo de variables de entorno
│
├── models/               # Modelos de datos
│   ├── __init__.py
│   ├── autor.py          # Modelo de Autor
│   ├── libro.py          # Modelo de Libro
│   ├── genero.py         # Modelo de Género literario
│   ├── usuario.py        # Modelo de Usuario para autenticación
│   ├── libro_autor.py    # Modelo de relación Libro-Autor
│   └── libro_genero.py   # Modelo de relación Libro-Género
│
├── routes/               # Blueprints (rutas)
│   ├── __init__.py
│   ├── auth.py           # Endpoints para autenticación
│   ├── autores.py        # Endpoints para autores
│   ├── libros.py         # Endpoints para libros
│   └── generos.py        # Endpoints para géneros
│
└── requirements.txt      # Dependencias del proyecto
```

## Instalación y Ejecución
 Consulta el archivo [Instrucciones.md](./Instrucciones.md) para obtener instrucciones detalladas sobre cómo configurar y ejecutar la API.
 
 ## Pruebas con Postman
 Se incluye una colección de Postman con ejemplos de todas las operaciones disponibles. Importa la colección en Postman para probar rápidamente la API.
 

