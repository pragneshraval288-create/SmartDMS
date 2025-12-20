from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/")
@login_required
def index():
    # FINAL: reports are system-defined (no dummy redirect)
    if not (current_user.is_admin or current_user.is_manager):
        return render_template("reports/index.html", reports=[])

    reports = [
        {
            "name": "Document Uploads",
            "description": "Daily document upload statistics",
            "updated_at": datetime.utcnow()
        },
        {
            "name": "User Activity",
            "description": "Recent user actions and events",
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Storage Usage",
            "description": "Disk usage by stored documents",
            "updated_at": datetime.utcnow()
        }
    ]

    return render_template(
        "reports/index.html",
        reports=reports
    )
