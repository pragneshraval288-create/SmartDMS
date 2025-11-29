from .auth import bp as auth_bp
from .dashboard import bp as dashboard_bp
from .documents import bp as documents_bp
from .history import bp as history_bp
from .api import bp as api_bp
from .profile import bp as profile_bp

__all__ = [
    "auth_bp",
    "dashboard_bp",
    "documents_bp",
    "history_bp",
    "api_bp",
    "profile_bp"
]
