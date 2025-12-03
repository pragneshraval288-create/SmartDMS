from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from backend.models.models import Document, Audit

bp = Blueprint("dashboard", __name__, url_prefix="/")

IST = timedelta(hours=5, minutes=30)

@bp.route("/")
@bp.route("/dashboard")
@bp.route("/dashboard/")  #  Trailing slash supported to avoid 404
@login_required
def home():
    #  Convert UTC to IST for UI feel
    current_time = datetime.utcnow() + IST
    week_ago = current_time - timedelta(days=7)

    #  Weekly upload count
    week_uploads = Document.query.filter(Document.upload_date >= week_ago).count()

    #  Role based data
    if current_user.role == "admin":
        total_docs = Document.query.count()
        recent_activity = Audit.query.order_by(Audit.timestamp.desc()).limit(40).all()
    else:
        total_docs = Document.query.filter_by(uploader_id=current_user.id).count()
        recent_activity = Audit.query.filter_by(user_id=current_user.id).order_by(Audit.timestamp.desc()).limit(20).all()

    stats = {
        "total_docs": total_docs,
        "week_uploads": week_uploads
    }

    return render_template("dashboard.html", stats=stats, recent_activity=recent_activity, current_time=current_time)
