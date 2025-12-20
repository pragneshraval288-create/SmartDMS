from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import User, ActivityLog

users_bp = Blueprint("users", __name__, url_prefix="/users")


# ======================================================
# USER LIST (EXISTING – UNCHANGED LOGIC)
# ======================================================
@users_bp.route("/")
@login_required
def index():
    # basic access control (admin/manager)
    if not (current_user.is_admin or current_user.is_manager):
        return render_template(
            "users/index.html",
            users=[]
        )

    users = User.query.order_by(User.username.asc()).all()

    return render_template(
        "users/index.html",
        users=users
    )


# ======================================================
# ADMIN ACTIONS (NEW)
# ======================================================
@users_bp.route("/<int:user_id>/deactivate")
@login_required
def deactivate_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("users.index"))

    user = User.query.get_or_404(user_id)

    user.is_active = False

    db.session.add(
        ActivityLog(
            action="user_deactivated",
            user_id=current_user.id
        )
    )
    db.session.commit()

    flash(f"User '{user.username}' deactivated.", "warning")
    return redirect(url_for("users.index"))


@users_bp.route("/<int:user_id>/activate")
@login_required
def activate_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("users.index"))

    user = User.query.get_or_404(user_id)

    user.is_active = True
    user.is_approved = True

    db.session.add(
        ActivityLog(
            action="user_activated",
            user_id=current_user.id
        )
    )
    db.session.commit()

    flash(f"User '{user.username}' activated.", "success")
    return redirect(url_for("users.index"))
