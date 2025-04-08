from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, validate, ValidationError
from models import db
from models.genero import Genero
from routes.auth import admin_required

# Creación del Blueprint para géneros
generos_bp = Blueprint('generos', __name__, url_prefix='/api/generos')

# Schema para validación con marshmallow
class GeneroSchema(Schema):
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=50))
    descripcion = fields.String(required=False, allow_none=True)

genero_schema = GeneroSchema()

# Rutas para operaciones CRUD de géneros

@generos_bp.route('/', methods=['GET'])
def get_generos():
    """Obtener todos los géneros activos"""
    generos = Genero.query.filter_by(activo=True).all()
    return jsonify({
        'status': 'success',
        'data': [genero.to_dict() for genero in generos]
    }), 200

@generos_bp.route('/<int:genero_id>', methods=['GET'])
def get_genero(genero_id):
    """Obtener un género por su ID"""
    genero = Genero.query.get_or_404(genero_id, description='Género no encontrado')
    
    if not genero.activo:
        return jsonify({
            'status': 'error',
            'message': 'Género no encontrado'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': genero.to_dict()
    }), 200

@generos_bp.route('/', methods=['POST'])
@jwt_required()
def create_genero():
    """Crear un nuevo género"""
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'El contenido debe ser JSON'
        }), 415
    
    try:
        # Validar datos de entrada
        datos = genero_schema.load(request.json)
        
        # Verificar si ya existe un género con el mismo nombre
        existing_genero = Genero.query.filter_by(nombre=datos['nombre']).first()
        if existing_genero:
            # Si existe pero está inactivo, reactivarlo
            if not existing_genero.activo:
                existing_genero.activo = True
                existing_genero.descripcion = datos.get('descripcion', existing_genero.descripcion)
                db.session.commit()
                return jsonify({
                    'status': 'success',
                    'message': 'Género reactivado exitosamente',
                    'data': existing_genero.to_dict()
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': f'Ya existe un género con el nombre {datos["nombre"]}'
                }), 400
        
        # Crear nuevo género
        nuevo_genero = Genero(
            nombre=datos['nombre'],
            descripcion=datos.get('descripcion')
        )
        
        # Guardar en la base de datos
        db.session.add(nuevo_genero)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Género creado exitosamente',
            'data': nuevo_genero.to_dict()
        }), 201
        
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'errors': err.messages
        }), 400

@generos_bp.route('/<int:genero_id>', methods=['PUT'])
@jwt_required()
def update_genero(genero_id):
    """Actualizar un género existente"""
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'El contenido debe ser JSON'
        }), 415
    
    genero = Genero.query.get_or_404(genero_id, description='Género no encontrado')
    
    if not genero.activo:
        return jsonify({
            'status': 'error',
            'message': 'Género no encontrado'
        }), 404
    
    try:
        # Validar datos de entrada
        datos = genero_schema.load(request.json)
        
        # Verificar si ya existe otro género con el mismo nombre
        if datos['nombre'] != genero.nombre:
            existing_genero = Genero.query.filter_by(nombre=datos['nombre']).first()
            if existing_genero:
                return jsonify({
                    'status': 'error',
                    'message': f'Ya existe un género con el nombre {datos["nombre"]}'
                }), 400
        
        # Actualizar género
        genero.nombre = datos['nombre']
        genero.descripcion = datos.get('descripcion', genero.descripcion)
        
        # Guardar cambios
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Género actualizado exitosamente',
            'data': genero.to_dict()
        }), 200
        
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'errors': err.messages
        }), 400

@generos_bp.route('/<int:genero_id>', methods=['DELETE'])
@jwt_required()
def delete_genero(genero_id):
    """Eliminar un género (borrado lógico)"""
    genero = Genero.query.get_or_404(genero_id, description='Género no encontrado')
    
    if not genero.activo:
        return jsonify({
            'status': 'error',
            'message': 'Género no encontrado'
        }), 404
    
    # Verificar si el género tiene libros asociados
    if len(genero.libros) > 0:
        return jsonify({
            'status': 'error',
            'message': 'No se puede eliminar el género porque tiene libros asociados'
        }), 400
    
    # Borrado lógico
    genero.activo = False
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Género eliminado exitosamente'
    }), 200

@generos_bp.route('/<int:genero_id>/libros', methods=['GET'])
def get_genero_libros(genero_id):
    """Obtener todos los libros de un género"""
    genero = Genero.query.get_or_404(genero_id, description='Género no encontrado')
    
    if not genero.activo:
        return jsonify({
            'status': 'error',
            'message': 'Género no encontrado'
        }), 404
    
    # Obtener los libros activos de este género
    libros = [lg.libro for lg in genero.libros if lg.libro.activo]
    
    return jsonify({
        'status': 'success',
        'data': [libro.to_dict() for libro in libros]
    }), 200