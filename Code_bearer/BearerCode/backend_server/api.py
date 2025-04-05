import os
from flask import Flask, jsonify, request, render_template
import jwt
from functools import wraps

# Definir la ubicación de la carpeta de templates
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Ruta de backend_server/
TEMPLATES_DIR = os.path.join(BASE_DIR, "../auth_server/templates")  # Ruta a templates/

# Inicializar Flask con la carpeta de templates corregida
app = Flask(__name__, template_folder=TEMPLATES_DIR)
app.config['SECRET_KEY'] = 'LaSalle2025'

# Decorador para requerir token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token no proporcionado'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except:
            return jsonify({'message': 'Token inválido o expirado'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Ruta protegida con token
@app.route('/api/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({
        'message': f'Acceso concedido para {current_user}',
        'data': 'Información protegida'
    })

# Ruta pública
@app.route('/api/public', methods=['GET'])
def public_route():
    return jsonify({'message': 'Acceso público'})

# Ruta para mostrar la página de prueba de token usando el template HTML
@app.route('/api/test-token', methods=['GET'])
def test_token_page():
    return render_template('test_token.html')  # Ahora usa un archivo HTML en templates/

# Ejecutar el servidor Flask
if __name__ == '__main__':
    app.run(port=5002)