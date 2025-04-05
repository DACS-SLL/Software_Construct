from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, validate, ValidationError
from models import db
from models.libro import Libro
from models.autor import Autor

# Creación del Blueprint para libros
libros_bp = Blueprint('libros', __name__, url_prefix='/api/libros')

# Schema para validación con marshmallow
class LibroSchema(Schema):
    titulo = fields.String(required=True, validate=validate.Length(min=1, max=100))
    isbn = fields.String(required=False, allow_none=True, validate=validate.Length(max=20))
    anio_publicacion = fields.Integer(required=False, allow_none=True)
    genero = fields.String(required=False, allow_none=True, validate=validate.Length(max=50))
    sinopsis = fields.String(required=False, allow_none=True)
    paginas = fields.Integer(required=False, allow_none=True)
    autor_id = fields.Integer(required=True)

libro_schema = LibroSchema()

# Rutas para operaciones CRUD de libros

@libros_bp.route('/', methods=['GET'])
def get_libros():
    """Obtener todos los libros"""
    libros = Libro.query.all()
    return jsonify({
        'status': 'success',
        'data': [libro.to_dict() for libro in libros]
    }), 200

@libros_bp.route('/<int:libro_id>', methods=['GET'])
def get_libro(libro_id):
    """Obtener un libro por su ID"""
    libro = Libro.query.get_or_404(libro_id, description='Libro no encontrado')
    return jsonify({
        'status': 'success',
        'data': libro.to_dict()
    }), 200

@libros_bp.route('/', methods=['POST'])
def create_libro():
    """Crear un nuevo libro"""
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'El contenido debe ser JSON'
        }), 415
    
    try:
        # Validar datos de entrada
        datos = libro_schema.load(request.json)
        
        # Verificar que el autor existe
        autor = Autor.query.get(datos['autor_id'])
        if not autor:
            return jsonify({
                'status': 'error',
                'message': f'El autor con ID {datos["autor_id"]} no existe'
            }), 400
        
        # Verificar si el ISBN ya existe (si se proporciona)
        if datos.get('isbn'):
            existing_libro = Libro.query.filter_by(isbn=datos['isbn']).first()
            if existing_libro:
                return jsonify({
                    'status': 'error',
                    'message': f'Ya existe un libro con el ISBN {datos["isbn"]}'
                }), 400
        
        # Crear nuevo libro
        nuevo_libro = Libro(
            titulo=datos['titulo'],
            isbn=datos.get('isbn'),
            anio_publicacion=datos.get('anio_publicacion'),
            genero=datos.get('genero'),
            sinopsis=datos.get('sinopsis'),
            paginas=datos.get('paginas'),
            autor_id=datos['autor_id']
        )
        
        # Guardar en la base de datos
        db.session.add(nuevo_libro)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Libro creado exitosamente',
            'data': nuevo_libro.to_dict()
        }), 201
        
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'errors': err.messages
        }), 400

@libros_bp.route('/<int:libro_id>', methods=['PUT'])
def update_libro(libro_id):
    """Actualizar un libro existente"""
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'El contenido debe ser JSON'
        }), 415
    
    libro = Libro.query.get_or_404(libro_id, description='Libro no encontrado')
    
    try:
        # Validar datos de entrada
        datos = libro_schema.load(request.json)
        
        # Verificar que el autor existe
        autor = Autor.query.get(datos['autor_id'])
        if not autor:
            return jsonify({
                'status': 'error',
                'message': f'El autor con ID {datos["autor_id"]} no existe'
            }), 400
        
        # Verificar si el ISBN ya existe y no pertenece a este libro
        if datos.get('isbn') and datos['isbn'] != libro.isbn:
            existing_libro = Libro.query.filter_by(isbn=datos['isbn']).first()
            if existing_libro and existing_libro.id != libro_id:
                return jsonify({
                    'status': 'error',
                    'message': f'Ya existe un libro con el ISBN {datos["isbn"]}'
                }), 400
        
        # Actualizar libro
        libro.titulo = datos['titulo']
        libro.isbn = datos.get('isbn')
        libro.anio_publicacion = datos.get('anio_publicacion')
        libro.genero = datos.get('genero')
        libro.sinopsis = datos.get('sinopsis')
        libro.paginas = datos.get('paginas')
        libro.autor_id = datos['autor_id']
        
        # Guardar cambios
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Libro actualizado exitosamente',
            'data': libro.to_dict()
        }), 200
        
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'errors': err.messages
        }), 400

@libros_bp.route('/<int:libro_id>', methods=['DELETE'])
def delete_libro(libro_id):
    """Eliminar un libro"""
    libro = Libro.query.get_or_404(libro_id, description='Libro no encontrado')
    
    # Eliminar libro
    db.session.delete(libro)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Libro eliminado exitosamente'
    }), 200

@libros_bp.route('/buscar', methods=['GET'])
def search_libros():
    """Buscar libros por título o género"""
    titulo = request.args.get('titulo', '')
    genero = request.args.get('genero', '')
    
    query = Libro.query
    
    if titulo:
        query = query.filter(Libro.titulo.ilike(f'%{titulo}%'))
    
    if genero:
        query = query.filter(Libro.genero.ilike(f'%{genero}%'))
    
    libros = query.all()
    
    return jsonify({
        'status': 'success',
        'count': len(libros),
        'data': [libro.to_dict() for libro in libros]
    }), 200