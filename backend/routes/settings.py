from flask import Blueprint, render_template
from flask_login import login_required, current_user

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/")
@login_required
def index():
    # FINAL: only admin/manager can view settings
    if not (current_user.is_admin or current_user.is_manager):
        return render_template("settings/index.html", settings=[])

    # System settings (final, read-only view)
    settings = [
        {
            "key": "MAX_UPLOAD_SIZE",
            "value": "25 MB",
            "description": "Maximum allowed file upload size"
        },
        {
            "key": "ALLOWED_FILE_TYPES",
            "value": "pdf, docx, xlsx, png, jpg",
            "description": "Permitted document formats"
        },
        {
            "key": "SESSION_TIMEOUT",
            "value": "30 minutes",
            "description": "User session expiry duration"
        }
    ]

    return render_template(
        "settings/index.html",
        settings=settings
    )
