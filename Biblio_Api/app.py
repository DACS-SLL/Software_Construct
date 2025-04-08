import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import config
from models import db, jwt
from models.usuario import Usuario

# Importar blueprints
from routes.auth import auth_bp
from routes.autores import autores_bp
from routes.libros import libros_bp
from routes.generos import generos_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Configuración CORS corregida
    CORS(app, 
         resources={r"/*": {"origins": "*"}},  
         allow_headers=["Content-Type", "Authorization"],
         expose_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Configurar la aplicación
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(autores_bp)
    app.register_blueprint(libros_bp)
    app.register_blueprint(generos_bp)
    
    # Ruta para servir el archivo demo.html
    @app.route('/demo')
    def demo():
        return send_from_directory('.', 'demo.html')
    
    # Ruta raíz
    @app.route('/')
    def index():
        return jsonify({
            'message': 'API de Biblioteca Mejorada - Gestión de Autores, Libros y Géneros',
            'version': '2.0',
            'endpoints': {
                'auth': '/api/auth',
                'autores': '/api/autores',
                'libros': '/api/libros',
                'generos': '/api/generos'
            }
        })
    
    # Manejador de errores 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'message': 'Recurso no encontrado'
        }), 404
    
    # Manejador de errores 500
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'status': 'error',
            'message': 'Error interno del servidor'
        }), 500
    
    # Manejador de errores de JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'status': 'error',
            'message': 'El token ha expirado. Por favor, inicie sesión nuevamente.'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'status': 'error',
            'message': 'Token inválido. Por favor, inicie sesión nuevamente.'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'status': 'error',
            'message': 'Se requiere autenticación para acceder a este recurso.'
        }), 401
    
    return app

def create_initial_data(app):
    """Crear datos iniciales para la aplicación"""
    with app.app_context():
        try:
            # Verificar si ya existe un usuario administrador
            admin = Usuario.query.filter_by(username='admin').first()
            if not admin:
                admin = Usuario(
                    username='admin',
                    email='admin@biblioteca.com',
                    nombre='Administrador',
                    apellido='Sistema',
                    rol='admin'
                )
                admin.password = 'admin123'  # ¡Cambiar en producción!
                db.session.add(admin)
                db.session.commit()
                print('Usuario administrador creado: admin / admin123')
            
            # Crear algunos géneros si no existen
            generos_default = ['Novela', 'Ciencia Ficción', 'Fantasía', 'Historia', 'Biografía', 'Poesía']
            from models.genero import Genero
            
            for nombre in generos_default:
                genero = Genero.query.filter_by(nombre=nombre).first()
                if not genero:
                    genero = Genero(nombre=nombre)
                    db.session.add(genero)
            
            db.session.commit()
            print('Géneros iniciales creados')
            
        except Exception as e:
            db.session.rollback()
            print(f'Error al crear datos iniciales: {str(e)}')

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    # Crear las tablas de la base de datos si no existen
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada correctamente")
    
    # Crear datos iniciales
    create_initial_data(app)
    
    # Ejecutar la aplicación
    app.run(host='0.0.0.0', port=5000, debug=True)