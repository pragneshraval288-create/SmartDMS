# backend/__init__.py

import os
from flask import Flask

from .config import Config, TEMPLATE_DIR, STATIC_DIR
from .extensions import db, login_manager, limiter

# 👇 yaha apne blueprints import karo
from backend.routes.dashboard import bp as dashboard_bp
# baaki blueprints (auth, documents, etc.) bhi ho sakte hai

def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(
        __name__,
        template_folder=str(TEMPLATE_DIR),
        static_folder=str(STATIC_DIR),
    )

    # config, db, login, etc...

    # 👇 yaha register karo
    app.register_blueprint(dashboard_bp)

    return app
