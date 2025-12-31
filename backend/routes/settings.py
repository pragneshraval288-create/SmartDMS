from flask import Blueprint, render_template
from flask_login import login_required, current_user

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/")
@login_required
def index():

    # ==================================================
    # ADMIN VIEW → SYSTEM SETTINGS
    # ==================================================
    if current_user.is_admin:
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

    # ==================================================
    # USER VIEW → PROFILE / ACCOUNT SETTINGS
    # ==================================================
    settings = [
        {
            "key": "Username",
            "value": current_user.username,
            "description": "Your account username"
        },
        {
            "key": "Email",
            "value": current_user.email,
            "description": "Registered email address"
        },
        {
            "key": "Role",
            "value": "Admin" if current_user.is_admin else "User",
            "description": "Your account role"
        },
        {
            "key": "Account Status",
            "value": "Active" if current_user.is_active else "Disabled",
            "description": "Current account state"
        },
        {
            "key": "MFA Enabled",
            "value": "Yes" if current_user.mfa_enabled else "No",
            "description": "Multi-factor authentication status"
        }
    ]

    return render_template(
        "settings/index.html",
        settings=settings
    )
