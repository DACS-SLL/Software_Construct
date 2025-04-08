# Instrucciones para Ejecutar la API de Biblioteca Mejorada

## Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Postman (para probar la API)

## Configuración del entorno

1. **Clonar el repositorio**

```bash
git clone <URL_DEL_REPOSITORIO>
cd biblioteca_api
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

4. **Configurar las variables de entorno**

Copia el archivo `.env.example` a `.env` y edita los valores según sea necesario:

```bash
cp .env.example .env
```

Las variables principales a configurar son:
- `DATABASE_URL`: URL de conexión a la base de datos
- `JWT_SECRET_KEY`: Clave secreta para firmar tokens JWT
- `JWT_ACCESS_TOKEN_EXPIRES`: Tiempo de expiración de tokens (en segundos)

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

La API estará disponible en `http://localhost:5000`.

## Probar la API con Postman

1. **Importar la colección de Postman**
   - Abrir Postman
   - Hacer clic en "Importar"
   - Cargar el archivo `biblioteca_api_mejorada_collection.json` proporcionado en este repositorio

2. **Verificar que la variable de entorno esté configurada**
   - La colección utiliza una variable `{{base_url}}` que debe estar configurada a `http://localhost:5000`
   - La colección también utiliza una variable `{{auth_token}}` que se actualiza automáticamente al iniciar sesión

3. **Autenticarse**
   - Primero, ejecuta la petición "Inicio de Sesión" en la carpeta "Autenticación"
   - Usa las credenciales del usuario administrador creado automáticamente:
     - Username: `admin`
     - Password: `admin123`
   - El token JWT se guardará automáticamente en la variable `{{auth_token}}` para las siguientes peticiones

4. **Probar los endpoints**
   - Una vez autenticado, puedes probar todas las operaciones disponibles
   - Sigue un orden lógico para evitar errores (crear autores y géneros antes de crear libros, etc.)

## Estructura de la API

### Autenticación
- Debes autenticarte para acceder a los endpoints protegidos (POST, PUT, DELETE)
- Los endpoints de solo lectura (GET) están disponibles sin autenticación
- El token JWT debe enviarse en el encabezado `Authorization: Bearer <token>`

### Flujo de trabajo recomendado para pruebas
1. Inicia sesión para obtener el token JWT
2. Crea algunos géneros literarios (o usa los creados automáticamente)
3. Crea algunos autores
4. Crea libros, asociándolos con autores y géneros
5. Prueba las operaciones de búsqueda y filtrado
6. Prueba las operaciones para añadir/eliminar autores o géneros a libros existentes
7. Prueba el borrado lógico y verifica que los registros no aparezcan en las consultas

## Notas importantes
- Cuando se "elimina" un registro (autor, libro o género), en realidad se realiza un borrado lógico (se marca como inactivo)
- La API incluye validaciones para evitar operaciones inconsistentes (como eliminar un autor que tiene libros asociados)
- Los datos se devuelven en formato JSON con estructura consistente:
  ```json
  {
    "status": "success|error",
    "message": "Mensaje descriptivo",
    "data": {...} // Solo en respuestas exitosas
  }
  ```

## Solución de problemas comunes

### Error: "El token ha expirado"
- El token JWT tiene un tiempo de expiración (por defecto, 24 horas)
- Inicia sesión nuevamente para obtener un nuevo token

### Error: "No se puede eliminar el último autor de un libro"
- Un libro debe tener al menos un autor asociado
- Asigna un nuevo autor antes de eliminar el actual

### Error: "Ya existe un libro con el ISBN X"
- El ISBN debe ser único para cada libro
- Verifica que no estés duplicando un ISBN existente

### Error al crear la base de datos
- Verifica que la carpeta donde se creará la base de datos tenga permisos de escritura
- Asegúrate de que la URL de conexión en `.env` sea correcta

### No se pueden importar módulos
- Asegúrate de estar ejecutando la aplicación desde la raíz del proyecto
- Verifica que todas las dependencias estén instaladas correctamente