from .api import app

__all__ = ['app']

def create_backend_app():
    from .api import app
    return app