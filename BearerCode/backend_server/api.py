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

@app.route('/api/test-token', methods=['GET'])
def test_token_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Probar Token</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
            textarea { width: 100%; height: 100px; margin: 10px 0; }
            button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
            .result { margin-top: 20px; padding: 10px; border-radius: 5px; }
            .success { background-color: #dff0d8; color: #3c763d; }
            .error { background-color: #f2dede; color: #a94442; }
        </style>
    </head>
    <body>
        <h1>Probar Token</h1>
        <form id="tokenForm">
            <label for="token">Ingresa tu token:</label><br>
            <textarea id="token" name="token" placeholder="Pega tu token aquí"></textarea><br>
            <button type="submit">Probar Token</button>
        </form>
        <div id="result" class="result" style="display: none;"></div>
        
        <script>
            document.getElementById('tokenForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const token = document.getElementById('token').value;
                const resultDiv = document.getElementById('result');
                
                try {
                    const response = await fetch('/api/protected', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.className = 'result success';
                        resultDiv.innerHTML = `<strong>Éxito:</strong> ${data.message}`;
                    } else {
                        resultDiv.className = 'result error';
                        resultDiv.innerHTML = `<strong>Error:</strong> ${data.message}`;
                    }
                } catch (error) {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
                }
                
                resultDiv.style.display = 'block';
            });
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=5002)