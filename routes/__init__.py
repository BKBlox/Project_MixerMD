# routes/__init__.py

from .user_routes import user_bp
from .test_routes import test_bp

__all__ = ['user_bp', 'test_bp']