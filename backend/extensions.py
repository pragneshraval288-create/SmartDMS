from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import redirect, url_for, flash

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per hour"]
)

# ✅ Login page redirect binding (Dashboard 404 ko fix karega)
login_manager.login_view = "auth.login"
login_manager.login_message = None
login_manager.login_message_category = "warning"

# ✅ Unauthorized notification login page me hi show hogi
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Please log in to access this page.", "warning")
    return redirect(url_for("auth.login"))
