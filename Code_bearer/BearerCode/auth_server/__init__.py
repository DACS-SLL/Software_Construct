from .auth import app

__all__ = ['app']

def create_auth_app():
    from .auth import app
    return app