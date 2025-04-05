from flask import Blueprint, jsonify, request
from datetime import datetime
from marshmallow import Schema, fields, validate, ValidationError
from models import db
from models.autor import Autor

# Creación del Blueprint para autores
autores_bp = Blueprint('autores', __name__, url_prefix='/api/autores')

# Schema para validación con marshmallow
class AutorSchema(Schema):
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=50))
    apellido = fields.String(required=True, validate=validate.Length(min=1, max=50))
    fecha_nacimiento = fields.Date(required=False, allow_none=True)
    nacionalidad = fields.String(required=False, allow_none=True, validate=validate.Length(max=50))
    biografia = fields.String(required=False, allow_none=True)

autor_schema = AutorSchema()

# Rutas para operaciones CRUD de autores

@autores_bp.route('/', methods=['GET'])
def get_autores():
    """Obtener todos los autores"""
    autores = Autor.query.all()
    return jsonify({
        'status': 'success',
        'data': [autor.to_dict() for autor in autores]
    }), 200

@autores_bp.route('/<int:autor_id>', methods=['GET'])
def get_autor(autor_id):
    """Obtener un autor por su ID"""
    autor = Autor.query.get_or_404(autor_id, description='Autor no encontrado')
    return jsonify({
        'status': 'success',
        'data': autor.to_dict()
    }), 200

@autores_bp.route('/', methods=['POST'])
def create_autor():
    """Crear un nuevo autor"""
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'El contenido debe ser JSON'
        }), 415
    
    try:
        # Validar datos de entrada
        datos = autor_schema.load(request.json)
        
        # Crear nuevo autor
        nuevo_autor = Autor(
            nombre=datos['nombre'],
            apellido=datos['apellido'],
            fecha_nacimiento=datos.get('fecha_nacimiento'),
            nacionalidad=datos.get('nacionalidad'),
            biografia=datos.get('biografia')
        )
        
        # Guardar en la base de datos
        db.session.add(nuevo_autor)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Autor creado exitosamente',
            'data': nuevo_autor.to_dict()
        }), 201
        
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'errors': err.messages
        }), 400

@autores_bp.route('/<int:autor_id>', methods=['PUT'])
def update_autor(autor_id):
    """Actualizar un autor existente"""
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'El contenido debe ser JSON'
        }), 415
    
    autor = Autor.query.get_or_404(autor_id, description='Autor no encontrado')
    
    try:
        # Validar datos de entrada
        datos = autor_schema.load(request.json)
        
        # Actualizar autor
        autor.nombre = datos['nombre']
        autor.apellido = datos['apellido']
        autor.fecha_nacimiento = datos.get('fecha_nacimiento')
        autor.nacionalidad = datos.get('nacionalidad')
        autor.biografia = datos.get('biografia')
        
        # Guardar cambios
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Autor actualizado exitosamente',
            'data': autor.to_dict()
        }), 200
        
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'errors': err.messages
        }), 400

@autores_bp.route('/<int:autor_id>', methods=['DELETE'])
def delete_autor(autor_id):
    """Eliminar un autor"""
    autor = Autor.query.get_or_404(autor_id, description='Autor no encontrado')
    
    # Verificar si el autor tiene libros asociados
    if autor.libros.count() > 0:
        return jsonify({
            'status': 'error',
            'message': 'No se puede eliminar el autor porque tiene libros asociados'
        }), 400
    
    # Eliminar autor
    db.session.delete(autor)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Autor eliminado exitosamente'
    }), 200

@autores_bp.route('/<int:autor_id>/libros', methods=['GET'])
def get_autor_libros(autor_id):
    """Obtener todos los libros de un autor"""
    autor = Autor.query.get_or_404(autor_id, description='Autor no encontrado')
    
    libros = autor.libros.all()
    return jsonify({
        'status': 'success',
        'data': [libro.to_dict() for libro in libros]
    }), 200