from flask import Flask, jsonify, request
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LaSalle2025'

# Base de datos de usuarios simulada
users = {
    "usuario1": "password1",
    "usuario2": "password2"
}

@app.route('/oauth/token', methods=['POST'])
def login():
    auth = request.authorization
    
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Credenciales no proporcionadas"}), 401
    
    if auth.username not in users or users[auth.username] != auth.password:
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    token = jwt.encode({
        'user': auth.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({"token": token})

if __name__ == '__main__':
    app.run(port=5001)