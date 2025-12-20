from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+
from ..extensions import db

IST = ZoneInfo("Asia/Kolkata")


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # actual message text
    message = db.Column(
        db.String(255),
        nullable=False
    )

    # read / unread
    is_read = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        index=True
    )

    # stored in IST (India)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(IST)
    )

    # relationship
    user = db.relationship(
        "User",
        back_populates="notifications",
        lazy="select"
    )

    # ----------------------------
    # helper methods (safe)
    # ----------------------------
    def mark_read(self):
        self.is_read = True

    def to_dict(self):
        """Useful for future API / AJAX"""
        return {
            "id": self.id,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }

    def __repr__(self):
        return (
            f"<Notification id={self.id} "
            f"user_id={self.user_id} "
            f"is_read={self.is_read}>"
        )
