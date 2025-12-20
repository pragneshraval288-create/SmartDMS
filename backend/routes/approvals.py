from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Document, User, ActivityLog

approvals_bp = Blueprint("approvals", __name__, url_prefix="/approvals")


# ======================================================
# DOCUMENT APPROVALS (EXISTING – UNCHANGED)
# ======================================================
@approvals_bp.route("/")
@login_required
def index():
    # approvals only for admin / manager
    if not (current_user.is_admin or current_user.is_manager):
        return render_template("approvals/index.html", documents=[], users=[])

    documents = (
        Document.query
        .filter(Document.status.in_(["pending", "approved", "rejected"]))
        .order_by(Document.created_at.desc())
        .all()
    )

    # 🔹 NEW: pending users for approval
    users = (
        User.query
        .filter_by(is_approved=False)
        .order_by(User.created_at.asc())
        .all()
    )

    return render_template(
        "approvals/index.html",
        documents=documents,
        users=users
    )


# ======================================================
# USER APPROVAL ACTION (NEW)
# ======================================================
@approvals_bp.route("/user/<int:user_id>/approve")
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
            user_id=current_user.id
        )
    )

    db.session.commit()

    flash(f"User '{user.username}' approved successfully.", "success")
    return redirect(url_for("approvals.index"))


@approvals_bp.route("/user/<int:user_id>/reject")
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
            user_id=current_user.id
        )
    )

    db.session.commit()

    flash(f"User '{user.username}' rejected.", "warning")
    return redirect(url_for("approvals.index"))
