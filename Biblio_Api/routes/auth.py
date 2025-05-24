from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate, ValidationError
from models import db, jwt
from models.usuario import Usuario

# Creación del Blueprint para autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Schema para validación con marshmallow
class RegistroSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=64))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    nombre = fields.String(required=False, allow_none=True)
    apellido = fields.String(required=False, allow_none=True)
    rol = fields.String(validate=validate.OneOf(['admin', 'editor', 'usuario']), default='usuario')

class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

registro_schema = RegistroSchema()
login_schema = LoginSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar un nuevo usuario"""
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'El contenido debe ser JSON'
        }), 415
    
    try:
        # Validar datos de entrada
        datos = registro_schema.load(request.json)
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(username=datos['username']).first():
            return jsonify({
                'status': 'error',
                'message': f'El usuario {datos["username"]} ya existe'
            }), 400
            
        if Usuario.query.filter_by(email=datos['email']).first():
            return jsonify({
                'status': 'error',
                'message': f'El email {datos["email"]} ya está registrado'
            }), 400
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            username=datos['username'],
            email=datos['email'],
            nombre=datos.get('nombre'),
            apellido=datos.get('apellido'),
            rol=datos.get('rol', 'usuario')
        )
        nuevo_usuario.password = datos['password']  # Esto utiliza el setter que hashea la contraseña
        
        # Guardar en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        # Generar token
        access_token = create_access_token(identity=nuevo_usuario.id)
        
        return jsonify({
            'status': 'success',
            'message': 'Usuario creado exitosamente',
            'data': {
                'usuario': nuevo_usuario.to_dict(),
                'token': access_token
            }
        }), 201
        
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'errors': err.messages
        }), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'El contenido debe ser JSON'
        }), 415
    
    try:
        # Validar datos de entrada
        datos = login_schema.load(request.json)
        
        # Buscar usuario
        usuario = Usuario.query.filter_by(username=datos['username']).first()
        
        # Verificar usuario y contraseña
        if not usuario or not usuario.verify_password(datos['password']):
            return jsonify({
                'status': 'error',
                'message': 'Credenciales inválidas'
            }), 401
            
        if not usuario.activo:
            return jsonify({
                'status': 'error',
                'message': 'Usuario desactivado'
            }), 403
        
        # Generar token
        access_token = create_access_token(identity=usuario.id)
        
        return jsonify({
            'status': 'success',
            'message': 'Inicio de sesión exitoso',
            'data': {
                'usuario': usuario.to_dict(),
                'token': access_token
            }
        }), 200
        
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'errors': err.messages
        }), 400

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Obtener perfil del usuario autenticado"""
    current_user_id = get_jwt_identity()
    usuario = Usuario.query.get_or_404(current_user_id)
    
    return jsonify({
        'status': 'success',
        'data': usuario.to_dict()
    }), 200

# Decorador personalizado para verificar roles
def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        usuario = Usuario.query.get_or_404(current_user_id)
        
        if usuario.rol != 'admin':
            return jsonify({
                'status': 'error',
                'message': 'Se requieren permisos de administrador'
            }), 403
            
        return fn(*args, **kwargs)
    
    wrapper.__name__ = fn.__name__
    return wrapper