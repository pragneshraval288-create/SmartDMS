from datetime import datetime
from flask_login import UserMixin
from backend.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    #  Login + Basic Profile
    username = db.Column(db.String(150), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    mobile = db.Column(db.String(20), unique=True, nullable=True)
    dob = db.Column(db.String(10), nullable=True)  # YYYY-MM-DD

    #  Profile Picture
    profile_pic = db.Column(db.String(200), default="default_user.png", nullable=True)

    #  Auth (HASHED password store hoga yaha)
    password_hash = db.Column(db.String(255), nullable=False)  # ✅ Added hash column
    # password = db.Column(db.String(200), nullable=False)  ❌ Raw password remove kiya

    #  Role
    role = db.Column(db.String(20), default="user")  # 'user' OR 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #  Relationship (Audit, Dashboard, History me uploader ka naam milega)
    documents = db.relationship("Document", backref="uploader", lazy=True)

    # Flask-Login ke liye required method (optional but recommended)
    def get_id(self):
        return str(self.id)


class Document(db.Model):
    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    filename = db.Column(db.String(200), nullable=False)

    #  Relationship stable rahe
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    tags = db.Column(db.String(200), nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    version = db.Column(db.Integer, default=1)


class Audit(db.Model):
    __tablename__ = "audit"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    action = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(200), nullable=True)
    version = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    #  Relationship FIXED — audit me user object se name access ho jayega
    user = db.relationship("User", backref="activities", lazy=True)
