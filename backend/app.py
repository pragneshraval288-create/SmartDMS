import os
from datetime import timezone
from zoneinfo import ZoneInfo

from flask import Flask, redirect, url_for
from flask_login import current_user

from .config import Config
from .extensions import db, login_manager, csrf
from .models import Notification

# --------------------------------------------------
# CORE ROUTES
# --------------------------------------------------
from .routes.auth import auth_bp
from .routes.document import document_bp
from .routes.folder import folder_bp
from .routes.dashboard import dashboard_bp
from .routes.api import api_bp
from .routes.profile import profile_bp

# 🔥 RECYCLE BIN
from .routes.recycle_bin import recycle_bin_bp

# --------------------------------------------------
# SIDEBAR MODULES
# --------------------------------------------------
from .routes.archive import archive_bp
from .routes.sharing import sharing_bp
from .routes.favorites import favorites_bp
from .routes.users import users_bp
from .routes.roles import roles_bp
from .routes.reports import reports_bp
from .routes.approvals import approvals_bp
from .routes.settings import settings_bp
from .routes.storage import storage_bp
from .routes.security import security_bp
from .routes.notifications import notifications_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    app.config.from_object(Config)

    # --------------------------------------------------
    # ENSURE REQUIRED FOLDERS
    # --------------------------------------------------
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )

    os.makedirs(os.path.join(project_root, "instance"), exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # --------------------------------------------------
    # INIT EXTENSIONS
    # --------------------------------------------------
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    # --------------------------------------------------
    # CREATE TABLES
    # --------------------------------------------------
    with app.app_context():
        db.create_all()

    # --------------------------------------------------
    # JINJA FILTER: IST
    # --------------------------------------------------
    @app.template_filter("ist")
    def ist_time(dt):
        if not dt:
            return "-"
        return (
            dt.replace(tzinfo=timezone.utc)
            .astimezone(ZoneInfo("Asia/Kolkata"))
            .strftime("%Y-%m-%d %H:%M")
        )

    # --------------------------------------------------
    # GLOBAL CONTEXT: NOTIFICATIONS
    # --------------------------------------------------
    @app.context_processor
    def inject_notifications():
        if current_user.is_authenticated:
            unread = (
                Notification.query
                .filter_by(
                    user_id=current_user.id,
                    is_read=False
                )
                .order_by(Notification.created_at.desc())
                .limit(10)
                .all()
            )
        else:
            unread = []

        return dict(unread_notifications=unread)

    # --------------------------------------------------
    # REGISTER BLUEPRINTS
    # --------------------------------------------------

    # CORE
    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(folder_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(api_bp)

    # 🔥 RECYCLE BIN
    app.register_blueprint(recycle_bin_bp)

    # SIDEBAR
    app.register_blueprint(archive_bp)
    app.register_blueprint(sharing_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(approvals_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(storage_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(notifications_bp)

    # --------------------------------------------------
    # HOME
    # --------------------------------------------------
    @app.route("/")
    def home():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.index"))
        return redirect(url_for("auth.login"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
