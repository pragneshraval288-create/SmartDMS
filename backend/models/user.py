from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for

from ..extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # -----------------------
    # BASIC INFO
    # -----------------------
    username = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    full_name = db.Column(
        db.String(255),
        nullable=True
    )

    profile_image = db.Column(
        db.String(255),
        nullable=True
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    # -----------------------
    # SECURITY
    # -----------------------
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # 🔥 ROLE SIMPLIFIED (admin / user ONLY)
    role = db.Column(
        db.String(20),
        nullable=False,
        default="user"
    )

    preferred_language = db.Column(
        db.String(10),
        default="en"
    )

    mfa_enabled = db.Column(db.Boolean, default=False)

    # USER STATE
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # -------------------------------------------------
    # RELATIONSHIPS
    # -------------------------------------------------
    documents = db.relationship(
        "Document",
        back_populates="uploader",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="select"
    )

    comments = db.relationship(
        "DocumentComment",
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="select"
    )

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="select"
    )

    # -----------------------
    # PASSWORD HANDLING
    # -----------------------
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(
            password,
            method="pbkdf2:sha256",
            salt_length=16
        )

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # -----------------------
    # ROLE HELPERS
    # -----------------------
    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    # -----------------------
    # PROFILE IMAGE HELPER
    # -----------------------
    @property
    def profile_image_url(self) -> str:
        if self.profile_image:
            return url_for(
                "static",
                filename=f"uploads/profile/{self.profile_image}"
            )
        return url_for(
            "static",
            filename="image/default-avatar.png"
        )

    def __repr__(self):
        return f"<User id={self.id} username={self.username} role={self.role}>"


# ======================
# LOGIN LOG (OPTIONAL)
# ======================
class LoginLog(db.Model):
    __tablename__ = "login_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    username_or_email = db.Column(db.String(255))
    success = db.Column(db.Boolean, default=False)

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    ip_address = db.Column(db.String(50))


# -----------------------
# FLASK-LOGIN USER LOADER
# -----------------------
@login_manager.user_loader
def load_user(user_id: str):
    try:
        return User.query.get(int(user_id))
    except (TypeError, ValueError):
        return None
