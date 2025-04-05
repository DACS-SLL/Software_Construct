import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from config import config
from models import db
from routes.autores import autores_bp
from routes.libros import libros_bp

def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Extensiones
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Blueprints
    app.register_blueprint(autores_bp)
    app.register_blueprint(libros_bp)
    
    # Raíz
    @app.route('/')
    def index():
        return jsonify({
            'message': 'API de Biblioteca - Gestión de Autores y Libros',
            'version': '1.0',
            'endpoints': {
                'autores': '/api/autores',
                'libros': '/api/libros'
            }
        })
    
    # Errores 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'message': 'Recurso no encontrado'
        }), 404
    
    # Errores 500
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'status': 'error',
            'message': 'Error interno del servidor'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    app.run(host='0.0.0.0', port=5000, debug=True)