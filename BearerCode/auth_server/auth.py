from flask import Flask, jsonify, request, render_template, redirect, url_for
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LaSalle2025'

users = {
    "jerson": "enyel123",
    "daniel": "gatitaNox",
    "juan": "LaSalle2025",
    "fernando": "LaSalle2025",
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_form():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return render_template('login.html', error="Usuario y contraseña requeridos")
    
    if username not in users or users[username] != password:
        return render_template('login.html', error="Credenciales inválidas")
    
    token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return render_template('token.html', token=token.decode('utf-8') if isinstance(token, bytes) else token)

@app.route('/oauth/token', methods=['POST'])
def login_api():
    auth = request.authorization
    
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Credenciales no proporcionadas"}), 401
    
    if auth.username not in users or users[auth.username] != auth.password:
        return jsonify({"message": "Credenciales inválidas"}), 401
    
    token = jwt.encode({
        'user': auth.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({"token": token.decode('utf-8') if isinstance(token, bytes) else token})

if __name__ == '__main__':
    app.run(port=5001)