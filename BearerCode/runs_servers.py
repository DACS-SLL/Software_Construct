from auth_server.auth import app as auth_app
from backend_server.api import app as backend_app
import threading

def run_auth_server():
    auth_app.run(port=5001, host='0.0.0.0')

def run_backend_server():
    backend_app.run(port=5002, host='0.0.0.0')

if __name__ == '__main__':
    threading.Thread(target=run_auth_server, daemon=True).start()
    threading.Thread(target=run_backend_server, daemon=True).start()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nServidores detenidos.")