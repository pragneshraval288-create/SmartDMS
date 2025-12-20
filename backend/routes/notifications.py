from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Notification

notifications_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/notifications"
)

# -------------------------------------------------
# Notifications Page
# -------------------------------------------------
@notifications_bp.route("/")
@login_required
def index():
    notifications = (
        Notification.query
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return render_template(
        "notifications/index.html",
        notifications=notifications
    )

# -------------------------------------------------
# Mark all as read (used by bell dropdown)
# -------------------------------------------------
@notifications_bp.route("/mark-read", methods=["POST"])
@login_required
def mark_read():
    (
        Notification.query
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read.is_(False)
        )
        .update({"is_read": True})
    )

    db.session.commit()
    return ("", 204)

# -------------------------------------------------
# Delete single notification (manual delete)
# -------------------------------------------------
@notifications_bp.route("/delete/<int:notification_id>", methods=["POST"])
@login_required
def delete_notification(notification_id):
    notification = (
        Notification.query
        .filter_by(
            id=notification_id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    db.session.delete(notification)
    db.session.commit()

    # supports normal form submit & AJAX
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(success=True)

    return ("", 204)

# -------------------------------------------------
# Clear all notifications
# -------------------------------------------------
@notifications_bp.route("/clear-all", methods=["POST"])
@login_required
def clear_all():
    (
        Notification.query
        .filter(Notification.user_id == current_user.id)
        .delete(synchronize_session=False)
    )

    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(success=True)

    return ("", 204)
