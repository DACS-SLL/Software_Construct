# Instrucciones para Ejecutar la API de Biblioteca

## Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Postman (para probar la API)

## Configuración del entorno

1. **Clonar el repositorio**

```bash
git clone <URL_DEL_REPOSITORIO>
cd Biblio_Api
```

2. **Crear un entorno virtual (opcional pero recomendado)**

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

4. **Configurar las variables de entorno (opcional)**

Puedes crear un archivo `.env` en la raíz del proyecto:

```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_CONFIG=development
```

## Inicializar la base de datos

1. **Crear las tablas de la base de datos**

```bash
flask db init
flask db migrate -m "Tablas iniciales"
flask db upgrade
```

## Ejecutar la aplicación

```bash
python app.py
```

O usando el comando `flask`:

```bash
flask run
```

La API estará disponible en `http://localhost:5000`. (También depende del puerto que quieras configurar en el dispositivo donde estés ejecutando la aplicación)

## Probar la API con Postman

1. **Importar la colección de Postman**
   - Abrir Postman
   - Hacer clic en "Importar"
   - Cargar el archivo de colección proporcionado en este repositorio

2. **Verificar que la variable de entorno esté configurada**
   - La colección utiliza una variable `{{base_url}}` que debe estar configurada a `http://localhost:5000`

3. **Probar los endpoints**
   - Primero crea un autor usando el endpoint `Crear autor`
   - Luego puedes crear libros asociados a ese autor

## Estructura de la API

### Endpoints de Autores
- `GET /api/autores`: Obtener todos los autores
- `GET /api/autores/{id}`: Obtener un autor por ID
- `POST /api/autores`: Crear un nuevo autor
- `PUT /api/autores/{id}`: Actualizar un autor existente
- `DELETE /api/autores/{id}`: Eliminar un autor
- `GET /api/autores/{id}/libros`: Obtener todos los libros de un autor

### Endpoints de Libros
- `GET /api/libros`: Obtener todos los libros
- `GET /api/libros/{id}`: Obtener un libro por ID
- `POST /api/libros`: Crear un nuevo libro
- `PUT /api/libros/{id}`: Actualizar un libro existente
- `DELETE /api/libros/{id}`: Eliminar un libro
- `GET /api/libros/buscar?titulo={titulo}&genero={genero}`: Buscar libros por título o género