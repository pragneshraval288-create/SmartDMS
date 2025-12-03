import os
import threading
import webbrowser
import logging

from flask import Flask, redirect, url_for
from flask_login import current_user, login_required

from backend.config import Config, TEMPLATE_DIR, STATIC_DIR
from backend.extensions import db, login_manager, migrate, csrf, limiter


def create_app():
    #  Flask app with correct template/static dirs
    app = Flask(
        __name__,
        template_folder=str(TEMPLATE_DIR),
        static_folder=str(STATIC_DIR),                                                     
    )

    #  Load config
    app.config.from_object(Config)

    #  Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    #  Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)

    #  Login redirect endpoint
    login_manager.login_view = "auth.login"

    #  current_user auto in templates
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    #  Register blueprints
    from backend.routes import auth, dashboard, documents, history, api, admin_users
    from backend.routes.profile import bp as profile_bp

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(documents.bp)
    app.register_blueprint(history.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_users.bp)

    #  Security headers
    @app.after_request
    def security_headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        resp.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        return resp

    #  Convenience route: /my-profile → correct profile view
    @app.route("/my-profile")
    @login_required
    def my_profile_redirect():
        return redirect(url_for("profile.profile_view"))

    #  Logging to file
    logging.basicConfig(
        filename="backend.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    return app


def open_browser():
    try:
        webbrowser.open_new("http://127.0.0.1:5000/")
    except Exception:
        pass


def main():
    app = create_app()

    #  Auto-open browser after server starts
    threading.Timer(1.0, open_browser).start()

    with app.app_context():
        db.create_all()

    #  Fixed host/port
    app.run(debug=True, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
