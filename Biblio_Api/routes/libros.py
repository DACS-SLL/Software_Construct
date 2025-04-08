from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, validate, ValidationError
from flask_jwt_extended import jwt_required
from models import db
from models.libro import Libro
from models.autor import Autor
from models.genero import Genero
from models.libro_autor import LibroAutor
from models.libro_genero import LibroGenero
from routes.auth import admin_required

# Creación del Blueprint para libros
libros_bp = Blueprint('libros', __name__, url_prefix='/api/libros')

# Schema para validación con marshmallow
class LibroSchema(Schema):
    titulo = fields.String(required=True, validate=validate.Length(min=1, max=100))
    isbn = fields.String(required=False, allow_none=True, validate=validate.Length(max=20))
    anio_publicacion = fields.Integer(required=False, allow_none=True)
    sinopsis = fields.String(required=False, allow_none=True)
    paginas = fields.Integer(required=False, allow_none=True)
    autores = fields.List(fields.Dict(keys=fields.Str(), values=fields.Raw()), required=False)
    generos = fields.List(fields.Integer(), required=False)

libro_schema = LibroSchema()

# Rutas para operaciones CRUD de libros

@libros_bp.route('/', methods=['GET'])
def get_libros():
    """Obtener todos los libros activos"""
    libros = Libro.query.filter_by(activo=True).all()
    return jsonify({
        'status': 'success',
        'data': [libro.to_dict(include_autores=True, include_generos=True) for libro in libros]
    }), 200

@libros_bp.route('/<int:libro_id>', methods=['GET'])
def get_libro(libro_id):
    """Obtener un libro por su ID"""
    libro = Libro.query.get_or_404(libro_id, description='Libro no encontrado')
    
    if not libro.activo:
        return jsonify({
            'status': 'error',
            'message': 'Libro no encontrado'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': libro.to_dict(include_autores=True, include_generos=True)
    }), 200

@libros_bp.route('/', methods=['POST'])
@jwt_required()
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
            sinopsis=datos.get('sinopsis'),
            paginas=datos.get('paginas')
        )
        
        # Guardar en la base de datos
        db.session.add(nuevo_libro)
        db.session.flush()  # Para obtener el ID del libro
        
        # Procesar autores
        if 'autores' in datos and datos['autores']:
            for autor_data in datos['autores']:
                autor_id = autor_data.get('id')
                rol = autor_data.get('rol')
                
                # Verificar que el autor existe
                autor = Autor.query.get(autor_id)
                if not autor or not autor.activo:
                    db.session.rollback()
                    return jsonify({
                        'status': 'error',
                        'message': f'El autor con ID {autor_id} no existe o está inactivo'
                    }), 400
                
                # Crear relación libro-autor
                libro_autor = LibroAutor(
                    libro_id=nuevo_libro.id,
                    autor_id=autor_id,
                    rol=rol
                )
                db.session.add(libro_autor)
        else:
            # Al menos un autor es requerido
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': 'Se requiere al menos un autor para el libro'
            }), 400
        
        # Procesar géneros
        if 'generos' in datos and datos['generos']:
            for genero_id in datos['generos']:
                # Verificar que el género existe
                genero = Genero.query.get(genero_id)
                if not genero or not genero.activo:
                    db.session.rollback()
                    return jsonify({
                        'status': 'error',
                        'message': f'El género con ID {genero_id} no existe o está inactivo'
                    }), 400
                
                # Crear relación libro-género
                libro_genero = LibroGenero(
                    libro_id=nuevo_libro.id,
                    genero_id=genero_id
                )
                db.session.add(libro_genero)
        
        # Confirmar transacción
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Libro creado exitosamente',
            'data': nuevo_libro.to_dict(include_autores=True, include_generos=True)
        }), 201
        
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'errors': err.messages
        }), 400

@libros_bp.route('/<int:libro_id>', methods=['PUT'])
@jwt_required()
def update_libro(libro_id):
    """Actualizar un libro existente"""
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'El contenido debe ser JSON'
        }), 415
    
    libro = Libro.query.get_or_404(libro_id, description='Libro no encontrado')
    
    if not libro.activo:
        return jsonify({
            'status': 'error',
            'message': 'Libro no encontrado'
        }), 404
    
    try:
        # Validar datos de entrada
        datos = libro_schema.load(request.json)
        
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
        libro.sinopsis = datos.get('sinopsis')
        libro.paginas = datos.get('paginas')
        
        # Procesar autores si se proporcionan
        if 'autores' in datos:
            # Eliminar relaciones existentes
            LibroAutor.query.filter_by(libro_id=libro_id).delete()
            
            # Agregar nuevas relaciones
            for autor_data in datos['autores']:
                autor_id = autor_data.get('id')
                rol = autor_data.get('rol')
                
                # Verificar que el autor existe
                autor = Autor.query.get(autor_id)
                if not autor or not autor.activo:
                    db.session.rollback()
                    return jsonify({
                        'status': 'error',
                        'message': f'El autor con ID {autor_id} no existe o está inactivo'
                    }), 400
                
                # Crear relación libro-autor
                libro_autor = LibroAutor(
                    libro_id=libro_id,
                    autor_id=autor_id,
                    rol=rol
                )
                db.session.add(libro_autor)
            
            # Verificar que al menos queda un autor
            if not datos['autores']:
                db.session.rollback()
                return jsonify({
                    'status': 'error',
                    'message': 'Se requiere al menos un autor para el libro'
                }), 400
        
        # Procesar géneros si se proporcionan
        if 'generos' in datos:
            # Eliminar relaciones existentes
            LibroGenero.query.filter_by(libro_id=libro_id).delete()
            
            # Agregar nuevas relaciones
            for genero_id in datos['generos']:
                # Verificar que el género existe
                genero = Genero.query.get(genero_id)
                if not genero or not genero.activo:
                    db.session.rollback()
                    return jsonify({
                        'status': 'error',
                        'message': f'El género con ID {genero_id} no existe o está inactivo'
                    }), 400
                
                # Crear relación libro-género
                libro_genero = LibroGenero(
                    libro_id=libro_id,
                    genero_id=genero_id
                )
                db.session.add(libro_genero)
        
        # Guardar cambios
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Libro actualizado exitosamente',
            'data': libro.to_dict(include_autores=True, include_generos=True)
        }), 200
        
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'errors': err.messages
        }), 400

@libros_bp.route('/<int:libro_id>', methods=['DELETE'])
@jwt_required()
def delete_libro(libro_id):
    """Eliminar un libro (borrado lógico)"""
    libro = Libro.query.get_or_404(libro_id, description='Libro no encontrado')
    
    if not libro.activo:
        return jsonify({
            'status': 'error',
            'message': 'Libro no encontrado'
        }), 404
    
    # Borrado lógico
    libro.activo = False
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Libro eliminado exitosamente'
    }), 200

@libros_bp.route('/buscar', methods=['GET'])
def search_libros():
    """Buscar libros por título, autor o género"""
    titulo = request.args.get('titulo', '')
    autor = request.args.get('autor', '')
    genero = request.args.get('genero', '')
    
    query = Libro.query.filter_by(activo=True)
    
    if titulo:
        query = query.filter(Libro.titulo.ilike(f'%{titulo}%'))
    
    if autor:
        query = query.join(LibroAutor).join(Autor).filter(
            Autor.activo == True,
            (Autor.nombre.ilike(f'%{autor}%') | Autor.apellido.ilike(f'%{autor}%'))
        )
    
    if genero:
        query = query.join(LibroGenero).join(Genero).filter(
            Genero.activo == True,
            Genero.nombre.ilike(f'%{genero}%')
        )
    
    libros = query.all()
    
    return jsonify({
        'status': 'success',
        'count': len(libros),
        'data': [libro.to_dict(include_autores=True, include_generos=True) for libro in libros]
    }), 200

@libros_bp.route('/<int:libro_id>/autores', methods=['GET'])
def get_libro_autores(libro_id):
    """Obtener todos los autores de un libro"""
    libro = Libro.query.get_or_404(libro_id, description='Libro no encontrado')
    
    if not libro.activo:
        return jsonify({
            'status': 'error',
            'message': 'Libro no encontrado'
        }), 404
    
    # Obtener los autores activos de este libro
    autores = [la.autor for la in libro.autores if la.autor.activo]
    
    return jsonify({
        'status': 'success',
        'data': [autor.to_dict() for autor in autores]
    }), 200

@libros_bp.route('/<int:libro_id>/generos', methods=['GET'])
def get_libro_generos(libro_id):
    """Obtener todos los géneros de un libro"""
    libro = Libro.query.get_or_404(libro_id, description='Libro no encontrado')
    
    if not libro.activo:
        return jsonify({
            'status': 'error',
            'message': 'Libro no encontrado'
        }), 404
    
    # Obtener los géneros activos de este libro
    generos = [lg.genero for lg in libro.generos if lg.genero.activo]
    
    return jsonify({
        'status': 'success',
        'data': [genero.to_dict() for genero in generos]
    }), 200

@libros_bp.route('/<int:libro_id>/autores/<int:autor_id>', methods=['POST'])
@jwt_required()
def add_autor_to_libro(libro_id, autor_id):
    """Asociar un autor a un libro"""
    libro = Libro.query.get_or_404(libro_id, description='Libro no encontrado')
    autor = Autor.query.get_or_404(autor_id, description='Autor no encontrado')
    
    if not libro.activo or not autor.activo:
        return jsonify({
            'status': 'error',
            'message': 'Libro o autor no encontrado'
        }), 404
    
    # Verificar si ya existe la relación
    rel = LibroAutor.query.filter_by(libro_id=libro_id, autor_id=autor_id).first()
    if rel:
        return jsonify({
            'status': 'error',
            'message': 'El autor ya está asociado a este libro'
        }), 400
    
    # Obtener el rol (si se proporciona)
    rol = request.json.get('rol') if request.is_json else None
    
    # Crear la relación
    nueva_rel = LibroAutor(
        libro_id=libro_id,
        autor_id=autor_id,
        rol=rol
    )
    
    db.session.add(nueva_rel)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Autor asociado al libro exitosamente'
    }), 201

@libros_bp.route('/<int:libro_id>/generos/<int:genero_id>', methods=['POST'])
@jwt_required()
def add_genero_to_libro(libro_id, genero_id):
    """Asociar un género a un libro"""
    libro = Libro.query.get_or_404(libro_id, description='Libro no encontrado')
    genero = Genero.query.get_or_404(genero_id, description='Género no encontrado')
    
    if not libro.activo or not genero.activo:
        return jsonify({
            'status': 'error',
            'message': 'Libro o género no encontrado'
        }), 404
    
    # Verificar si ya existe la relación
    rel = LibroGenero.query.filter_by(libro_id=libro_id, genero_id=genero_id).first()
    if rel:
        return jsonify({
            'status': 'error',
            'message': 'El género ya está asociado a este libro'
        }), 400
    
    # Crear la relación
    nueva_rel = LibroGenero(
        libro_id=libro_id,
        genero_id=genero_id
    )
    
    db.session.add(nueva_rel)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Género asociado al libro exitosamente'
    }), 201

@libros_bp.route('/<int:libro_id>/autores/<int:autor_id>', methods=['DELETE'])
@jwt_required()
def remove_autor_from_libro(libro_id, autor_id):
    """Eliminar la asociación entre un libro y un autor"""
    rel = LibroAutor.query.filter_by(libro_id=libro_id, autor_id=autor_id).first_or_404(
        description='Relación no encontrada'
    )
    
    # Verificar que no es el último autor
    if LibroAutor.query.filter_by(libro_id=libro_id).count() <= 1:
        return jsonify({
            'status': 'error',
            'message': 'No se puede eliminar el último autor de un libro'
        }), 400
    
    db.session.delete(rel)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Asociación eliminada exitosamente'
    }), 200

@libros_bp.route('/<int:libro_id>/generos/<int:genero_id>', methods=['DELETE'])
@jwt_required()
def remove_genero_from_libro(libro_id, genero_id):
    """Eliminar la asociación entre un libro y un género"""
    rel = LibroGenero.query.filter_by(libro_id=libro_id, genero_id=genero_id).first_or_404(
        description='Relación no encontrada'
    )
    
    db.session.delete(rel)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Asociación eliminada exitosamente'
    }), 200