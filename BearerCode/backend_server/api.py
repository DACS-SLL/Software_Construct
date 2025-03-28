from flask import Flask, jsonify, request
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LaSalle2025'

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

@app.route('/api/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({
        'message': f'Acceso concedido para {current_user}',
        'data': 'Información protegida'
    })

@app.route('/api/public', methods=['GET'])
def public_route():
    return jsonify({'message': 'Acceso público'})

if __name__ == '__main__':
    app.run(port=5002)