# API de Gestión de Biblioteca Mejorada

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
- Flask-JWT-Extended: Autenticación y autorización con tokens JWT
- Marshmallow: Validación de esquemas
- SQLite: Base de datos (para desarrollo, configurable para otras bases de datos en producción)
- Python-dotenv: Gestión de variables de entorno

## Estructura del proyecto
```

## Instalación y Ejecución

1. **Clonar el repositorio**

```bash
git clone <URL_DEL_REPOSITORIO>
cd biblioteca_api
```

2. **Configurar el entorno virtual (opcional pero recomendado)**

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar las variables de entorno**

Copia el archivo `.env.example` a `.env` y edita los valores según sea necesario:

```bash
cp .env.example .env
```

5. **Ejecutar la aplicación**

```bash
python app.py
```

La API estará disponible en `http://localhost:5000`.

## Autenticación

La API utiliza autenticación basada en tokens JWT. Para acceder a los endpoints protegidos:

1. Regístrate o inicia sesión para obtener un token:
   - `POST /api/auth/register` - Crear una nueva cuenta
   - `POST /api/auth/login` - Iniciar sesión con credenciales existentes

2. Incluye el token en las solicitudes a endpoints protegidos:
   - En el encabezado HTTP: `Authorization: Bearer <token>`

Nota: Al iniciar la aplicación por primera vez, se crea automáticamente un usuario administrador (usuario: `admin`, contraseña: `admin123`). **Se recomienda cambiar esta contraseña en un entorno de producción.**
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