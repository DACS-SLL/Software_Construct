# API de Gestión de Biblioteca

## Descripción
Esta es una API RESTful para gestionar autores y libros de una biblioteca. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre ambas entidades y establece relaciones entre ellas.

## Características
- Gestión completa de autores (crear, obtener, actualizar, eliminar)
- Gestión completa de libros (crear, obtener, actualizar, eliminar)
- Relación entre autores y libros (un autor puede tener muchos libros)
- Validación de datos de entrada con Marshmallow
- Manejo de errores HTTP
- Búsqueda de libros por título y género
- Implementación con blueprints para organizar el código

## Tecnologías utilizadas
- Flask: Framework web en Python
- SQLAlchemy: ORM para la base de datos
- Flask-Migrate: Migraciones de base de datos
- Marshmallow: Validación de esquemas
- SQLite: Base de datos (para desarrollo)

## Estructura del proyecto
```
biblioteca_api/
│
├── app.py                # Archivo principal de la aplicación
├── config.py             # Configuraciones de la aplicación
├── models/               # Modelos de datos
│   ├── __init__.py
│   ├── autor.py          # Modelo de Autor
│   └── libro.py          # Modelo de Libro
│
├── routes/               # Blueprints (rutas)
│   ├── __init__.py
│   ├── autores.py        # Endpoints para autores
│   └── libros.py         # Endpoints para libros
│
└── requirements.txt      # Dependencias del proyecto
```

## Instalación y Ejecución
Consulta el archivo [INSTRUCCIONES.md](./INSTRUCCIONES.md) para obtener instrucciones detalladas sobre cómo configurar y ejecutar la API.

## Pruebas con Postman
Se incluye una colección de Postman con ejemplos de todas las operaciones disponibles. Importa la colección en Postman para probar rápidamente la API.

## Modelo de datos

### Autor
- id: Identificador único (entero, clave primaria)
- nombre: Nombre del autor (cadena, requerido)
- apellido: Apellido del autor (cadena, requerido)
- fecha_nacimiento: Fecha de nacimiento (fecha, opcional)
- nacionalidad: Nacionalidad del autor (cadena, opcional)
- biografia: Biografía del autor (texto, opcional)
- fecha_creacion: Fecha de creación del registro (fecha/hora, automático)

### Libro
- id: Identificador único (entero, clave primaria)
- titulo: Título del libro (cadena, requerido)
- isbn: Número ISBN (cadena, único, opcional)
- anio_publicacion: Año de publicación (entero, opcional)
- genero: Género del libro (cadena, opcional)
- sinopsis: Sinopsis del libro (texto, opcional)
- paginas: Número de páginas (entero, opcional)
- autor_id: ID del autor (entero, clave foránea)
- fecha_creacion: Fecha de creación del registro (fecha/hora, automático)

## Endpoints de la API

### Autores
- `GET /api/autores`: Obtener todos los autores
- `GET /api/autores/{id}`: Obtener un autor por ID
- `POST /api/autores`: Crear un nuevo autor
- `PUT /api/autores/{id}`: Actualizar un autor existente
- `DELETE /api/autores/{id}`: Eliminar un autor
- `GET /api/autores/{id}/libros`: Obtener todos los libros de un autor

### Libros
- `GET /api/libros`: Obtener todos los libros
- `GET /api/libros/{id}`: Obtener un libro por ID
- `POST /api/libros`: Crear un nuevo libro
- `PUT /api/libros/{id}`: Actualizar un libro existente
- `DELETE /api/libros/{id}`: Eliminar un libro
- `GET /api/libros/buscar?titulo={titulo}&genero={genero}`: Buscar libros por título o género

## Ejemplos de uso

### Crear un autor
```http
POST /api/autores
Content-Type: application/json

{
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06",
    "nacionalidad": "Colombiana",
    "biografia": "Conocido como Gabo, fue un escritor, cuentista, guionista y periodista colombiano, premio Nobel de Literatura en 1982."
}
```

### Crear un libro
```http
POST /api/libros
Content-Type: application/json

{
    "titulo": "Cien años de soledad",
    "isbn": "978-0307474728",
    "anio_publicacion": 1967,
    "genero": "Realismo mágico",
    "sinopsis": "La historia de la familia Buendía a lo largo de siete generaciones en el pueblo ficticio de Macondo.",
    "paginas": 417,
    "autor_id": 1
}
```
