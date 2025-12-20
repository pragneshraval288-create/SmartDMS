# backend/extensions/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from sqlalchemy import event
from sqlalchemy.engine import Engine


# ------------------------------------------------------
# EXTENSIONS
# ------------------------------------------------------
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"


# ======================================================
# 🔐 DATABASE ENGINE SETTINGS (MYSQL SAFE)
# ======================================================
@event.listens_for(Engine, "connect")
def set_engine_options(dbapi_connection, connection_record):
    """
    This hook is intentionally kept generic.
    - SQLite-specific PRAGMA removed
    - MySQL already enforces foreign keys by default (InnoDB)
    - Safe for MySQL, PostgreSQL, future DBs
    """
    pass
