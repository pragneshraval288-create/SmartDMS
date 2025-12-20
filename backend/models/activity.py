from datetime import datetime, timedelta
from ..extensions import db

# IST offset (UTC + 5:30)
IST = timedelta(hours=5, minutes=30)


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)

    action = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    details = db.Column(db.Text, nullable=True)

    ip_address = db.Column(db.String(45), nullable=True)

    # 🔐 Always store UTC in DB
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # -----------------------
    # TIME HELPERS
    # -----------------------
    @property
    def ist_time(self):
        """
        Convert stored UTC time → IST for display
        """
        if self.created_at:
            return self.created_at + IST
        return None

    def __repr__(self):
        return (
            f"<ActivityLog id={self.id} "
            f"action={self.action} "
            f"user_id={self.user_id}>"
        )
