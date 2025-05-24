from flask import Blueprint, jsonify, request
from datetime import datetime
from marshmallow import Schema, fields, validate, ValidationError
from flask_jwt_extended import jwt_required
from models import db
from models.autor import Autor
from models.libro import Libro
from models.libro_autor import LibroAutor
from routes.auth import admin_required

# Creación del Blueprint para autores
autores_bp = Blueprint('autores', __name__, url_prefix='/api/autores')

# Schema para validación con marshmallow
class AutorSchema(Schema):
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=50))
    apellido = fields.String(required=True, validate=validate.Length(min=1, max=50))
    fecha_nacimiento = fields.Date(required=False, allow_none=True)
    nacionalidad = fields.String(required=False, allow_none=True, validate=validate.Length(max=50))
    biografia = fields.String(required=False, allow_none=True)
    activo = fields.Boolean(required=False, missing=True)

autor_schema = AutorSchema()

# Rutas para operaciones CRUD de autores

@autores_bp.route('/', methods=['GET'])
def get_autores():
    """Obtener autores, filtrando por estado si se proporciona"""
    estado = request.args.get('activo')  # Obtén el parámetro de consulta "activo"
    
    if estado is not None:
        estado = estado.lower() == 'true'  # Convierte el valor a booleano
        autores = Autor.query.filter_by(activo=estado).all()
    else:
        autores = Autor.query.all()  # Si no se proporciona, devuelve todos

    return jsonify({
        'status': 'success',
        'data': [autor.to_dict() for autor in autores]
    }), 200

@autores_bp.route('/<int:autor_id>', methods=['GET'])
def get_autor(autor_id):
    """Obtener un autor por su ID"""
    autor = Autor.query.get_or_404(autor_id, description='Autor no encontrado')
    
    if not autor.activo:
        return jsonify({
            'status': 'error',
            'message': 'Autor no encontrado'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': autor.to_dict(include_libros=True)
    }), 200

@autores_bp.route('/', methods=['POST'])
@jwt_required()
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

    except IntegrityError as err:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'El nombre del autor ya existe'
        }), 400

    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'errors': err.messages
        }), 400

@autores_bp.route('/<int:autor_id>', methods=['PUT'])
@jwt_required()
def update_autor(autor_id):
    """Actualizar un autor existente"""
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'El contenido debe ser JSON'
        }), 415

    autor = Autor.query.get_or_404(autor_id, description='Autor no encontrado')

    try:
        datos = autor_schema.load(request.json, partial=True)

        if not autor.activo and not datos.get('activo', False):
            return jsonify({
                'status': 'error',
                'message': 'Autor no encontrado'
            }), 404

        autor.nombre = datos.get('nombre', autor.nombre)
        autor.apellido = datos.get('apellido', autor.apellido)
        autor.fecha_nacimiento = datos.get('fecha_nacimiento', autor.fecha_nacimiento)
        autor.nacionalidad = datos.get('nacionalidad', autor.nacionalidad)
        autor.biografia = datos.get('biografia', autor.biografia)

        # Nueva línea para permitir actualizar el estado
        if 'activo' in datos:
            autor.activo = datos['activo']

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
@jwt_required()
def delete_autor(autor_id):
    """Eliminar un autor (borrado lógico)"""
    autor = Autor.query.get_or_404(autor_id, description='Autor no encontrado')
    
    if not autor.activo:
        return jsonify({
            'status': 'error',
            'message': 'Autor no encontrado'
        }), 404
    
    # Borrado lógico
    autor.activo = False
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Autor eliminado exitosamente'
    }), 200

@autores_bp.route('/<int:autor_id>/libros', methods=['GET'])
def get_autor_libros(autor_id):
    """Obtener todos los libros de un autor"""
    autor = Autor.query.get_or_404(autor_id, description='Autor no encontrado')
    
    if not autor.activo:
        return jsonify({
            'status': 'error',
            'message': 'Autor no encontrado'
        }), 404
    
    # Obtener los libros activos de este autor
    libros = [la.libro for la in autor.libros if la.libro.activo]
    
    return jsonify({
        'status': 'success',
        'data': [libro.to_dict() for libro in libros]
    }), 200

@autores_bp.route('/<int:autor_id>/libros/<int:libro_id>', methods=['POST'])
@jwt_required()
def add_libro_to_autor(autor_id, libro_id):
    """Asociar un libro existente a un autor"""
    autor = Autor.query.get_or_404(autor_id, description='Autor no encontrado')
    libro = Libro.query.get_or_404(libro_id, description='Libro no encontrado')
    
    if not autor.activo or not libro.activo:
        return jsonify({
            'status': 'error',
            'message': 'Autor o libro no encontrado'
        }), 404
    
    # Verificar si ya existe la relación
    rel = LibroAutor.query.filter_by(autor_id=autor_id, libro_id=libro_id).first()
    if rel:
        return jsonify({
            'status': 'error',
            'message': 'El libro ya está asociado a este autor'
        }), 400
    
    # Obtener el rol (si se proporciona)
    rol = request.json.get('rol') if request.is_json else None
    
    # Crear la relación
    nueva_rel = LibroAutor(
        autor_id=autor_id,
        libro_id=libro_id,
        rol=rol
    )
    
    db.session.add(nueva_rel)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Libro asociado al autor exitosamente'
    }), 201

@autores_bp.route('/<int:autor_id>/libros/<int:libro_id>', methods=['DELETE'])
@jwt_required()
def remove_libro_from_autor(autor_id, libro_id):
    """Eliminar la asociación entre un libro y un autor"""
    rel = LibroAutor.query.filter_by(autor_id=autor_id, libro_id=libro_id).first_or_404(
        description='Relación no encontrada'
    )
    
    db.session.delete(rel)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Asociación eliminada exitosamente'
    }), 200
