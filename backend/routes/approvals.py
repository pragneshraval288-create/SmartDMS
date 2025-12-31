from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import User, ActivityLog

approvals_bp = Blueprint("approvals", __name__, url_prefix="/approvals")


# ======================================================
# USER APPROVALS ONLY
# ======================================================
@approvals_bp.route("/")
@login_required
def index():
    if not current_user.is_admin:
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("dashboard.index"))

    users = (
        User.query
        .filter_by(is_approved=False)
        .order_by(User.created_at.asc())
        .all()
    )

    return render_template(
        "approvals/index.html",
        users=users
    )


# ======================================================
# USER APPROVE
# ======================================================
@approvals_bp.route("/user/<int:user_id>/approve", methods=["POST"])
@login_required
def approve_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("approvals.index"))

    user = User.query.get_or_404(user_id)

    user.is_approved = True
    user.is_active = True

    db.session.add(
        ActivityLog(
            action="user_approved",
            user_id=current_user.id,
            ip_address=request.remote_addr
        )
    )

    db.session.commit()

    flash(f"User '{user.username}' approved successfully.", "success")
    return redirect(url_for("approvals.index"))


# ======================================================
# USER REJECT
# ======================================================
@approvals_bp.route("/user/<int:user_id>/reject", methods=["POST"])
@login_required
def reject_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("approvals.index"))

    user = User.query.get_or_404(user_id)

    user.is_active = False
    user.is_approved = False

    db.session.add(
        ActivityLog(
            action="user_rejected",
            user_id=current_user.id,
            ip_address=request.remote_addr
        )
    )

    db.session.commit()

    flash(f"User '{user.username}' rejected.", "warning")
    return redirect(url_for("approvals.index"))
