from flask import current_app
from ..extensions import db
from ..models import Notification, User


def notify_user(user: User, message: str) -> None:
    """
    Create a notification for a user.
    """

    if not user:
        return

    if not current_app.config.get("ENABLE_NOTIFICATIONS", True):
        return

    note = Notification(
        user_id=user.id,
        message=message,
        is_read=False
    )

    db.session.add(note)
    db.session.commit()
