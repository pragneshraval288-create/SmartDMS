import os
from datetime import timezone, datetime
from zoneinfo import ZoneInfo

# 🔥 VERY IMPORTANT: .env MUST be loaded before Config
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, url_for
from flask_login import current_user, logout_user

# Configuration imports
from .config import Config
from .extensions import db, login_manager, csrf, migrate
from .models import Notification

# --------------------------------------------------
# BLUEPRINT IMPORTS
# --------------------------------------------------
from .routes.auth import auth_bp
from .routes.document import document_bp
from .routes.folder import folder_bp
from .routes.dashboard import dashboard_bp
from .routes.api import api_bp
from .routes.profile import profile_bp
from .routes.recycle_bin import recycle_bin_bp

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


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    # --------------------------------------------------
    # LOAD CONFIG
    # --------------------------------------------------
    app.config.from_object(config_class)

    # --------------------------------------------------
    # ENSURE REQUIRED FOLDERS
    # --------------------------------------------------
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Ensure instance folder exists
    os.makedirs(os.path.join(base_dir, "instance"), exist_ok=True)

    # Ensure upload folder exists
    upload_path = app.config.get("UPLOAD_FOLDER", "uploads")
    if not os.path.isabs(upload_path):
        upload_path = os.path.join(base_dir, upload_path)
    os.makedirs(upload_path, exist_ok=True)

    # --------------------------------------------------
    # INIT EXTENSIONS
    # --------------------------------------------------
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    # migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # --------------------------------------------------
    # DATABASE SETUP
    # --------------------------------------------------
    with app.app_context():
        db.create_all()

    # --------------------------------------------------
    # JINJA FILTER: IST (Timezone)
    # --------------------------------------------------
    @app.template_filter("ist")
    def ist_time(dt):
        if not dt:
            return "-"

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return (
            dt.astimezone(ZoneInfo("Asia/Kolkata"))
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
            return dict(unread_notifications=unread)

        return dict(unread_notifications=[])

    # --------------------------------------------------
    # REGISTER BLUEPRINTS
    # --------------------------------------------------
    blueprints = [
        auth_bp, document_bp, folder_bp, profile_bp, dashboard_bp, api_bp,
        recycle_bin_bp, archive_bp, sharing_bp, favorites_bp, users_bp,
        roles_bp, reports_bp, approvals_bp, settings_bp, storage_bp,
        security_bp, notifications_bp
    ]

    for bp in blueprints:
        app.register_blueprint(bp)

    # --------------------------------------------------
    # HOME ROUTE (FORCE LOGIN)
    # --------------------------------------------------
    @app.route("/")
    def home():
        """
        Force logout to ensure Login Page appears.
        """
        logout_user()
        return redirect(url_for("auth.login"))

    return app


# --------------------------------------------------
# APP ENTRY POINT
# --------------------------------------------------
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
