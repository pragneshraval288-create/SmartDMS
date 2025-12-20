from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import ActivityLog

security_bp = Blueprint("security", __name__, url_prefix="/security")


@security_bp.route("/")
@login_required
def index():
    # only admin / manager can view
    if not (current_user.is_admin or current_user.is_manager):
        return render_template("security/index.html", logs=[])

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
