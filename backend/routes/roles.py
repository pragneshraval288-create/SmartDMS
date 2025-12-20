from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from ..models import User

roles_bp = Blueprint("roles", __name__, url_prefix="/roles")


@roles_bp.route("/")
@login_required
def index():
    # FINAL: only admin/manager can view roles
    if not (current_user.is_admin or current_user.is_manager):
        return render_template("roles/index.html", roles=[])

    # Aggregate users by role
    rows = (
        User.query
        .with_entities(User.role, func.count(User.id))
        .group_by(User.role)
        .all()
    )

    roles = [
        {
            "name": role or "user",
            "description": None,
            "user_count": count
        }
        for role, count in rows
    ]

    return render_template(
        "roles/index.html",
        roles=roles
    )
