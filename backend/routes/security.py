from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import ActivityLog

security_bp = Blueprint("security", __name__, url_prefix="/security")


@security_bp.route("/")
@login_required
def index():

    # ==================================================
    # ADMIN VIEW → ALL SECURITY LOGS
    # ==================================================
    if current_user.is_admin:
        logs = (
            ActivityLog.query
            .order_by(ActivityLog.created_at.desc())
            .limit(50)
            .all()
        )

        return render_template(
            "security/index.html",
            logs=logs
        )

    # ==================================================
    # USER VIEW → OWN SECURITY / ACTIVITY LOGS
    # ==================================================
    logs = (
        ActivityLog.query
        .filter(ActivityLog.user_id == current_user.id)
        .order_by(ActivityLog.created_at.desc())
        .limit(50)
        .all()
    )

    return render_template(
        "security/index.html",
        logs=logs
    )
