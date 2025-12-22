from datetime import datetime, timedelta
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from ..models import (
    Document,
    User,
    ActivityLog,
    Notification,
    Folder
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)

FILE_TYPE_ORDER = [
    "pdf", "doc", "docx", "xls", "xlsx",
    "ppt", "pptx", "txt", "png", "jpg",
    "jpeg", "zip", "other"
]


@dashboard_bp.route("/", methods=["GET"])
@login_required
def index():

    # ------------------------------
    # BASE QUERIES (🔥 FIXED)
    # ------------------------------
    if current_user.is_admin:
        doc_query = Document.query.filter(
            Document.is_deleted.is_(False)
        )
        folder_query = Folder.query.filter(
            Folder.is_deleted.is_(False)
        )
    else:
        doc_query = Document.query.filter(
            Document.uploaded_by == current_user.id,
            Document.is_deleted.is_(False)
        )
        folder_query = Folder.query.filter(
            Folder.created_by == current_user.id,
            Folder.is_deleted.is_(False)
        )

    # ------------------------------
    # BASIC STATS
    # ------------------------------
    total_docs = doc_query.count()
    active_docs = doc_query.filter_by(is_active=True).count()
    archived_docs = doc_query.filter_by(is_active=False).count()
    total_users = User.query.count()
    total_folders = folder_query.count()

    one_week_ago = datetime.utcnow() - timedelta(days=7)
    uploads_week = doc_query.filter(
        Document.created_at >= one_week_ago
    ).count()

    # ------------------------------
    # EXPIRING DOCS
    # ------------------------------
    in_30_days = datetime.utcnow().date() + timedelta(days=30)
    expiring_docs = (
        doc_query
        .filter(
            Document.expiry_date.isnot(None),
            Document.expiry_date <= in_30_days
        )
        .order_by(Document.expiry_date.asc())
        .limit(5)
        .all()
    )

    # ------------------------------
    # RECENT DOCS
    # ------------------------------
    recent_docs = (
        doc_query
        .order_by(Document.created_at.desc())
        .limit(5)
        .all()
    )

    # ------------------------------
    # RECENT FOLDERS (🔥 FIXED)
    # ------------------------------
    recent_folders = (
        folder_query
        .filter(Folder.parent_id.is_(None))
        .order_by(Folder.created_at.desc())
        .limit(5)
        .all()
    )

    # ------------------------------
    # RECENT ACTIVITIES
    # ------------------------------
    if current_user.is_admin:
        recent_activities = (
            ActivityLog.query
            .order_by(ActivityLog.created_at.desc())
            .limit(10)
            .all()
        )
    else:
        recent_activities = (
            ActivityLog.query
            .filter(ActivityLog.user_id == current_user.id)
            .order_by(ActivityLog.created_at.desc())
            .limit(10)
            .all()
        )

    # ------------------------------
    # UPLOAD TREND
    # ------------------------------
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=9)

    uploads_raw = (
        doc_query
        .with_entities(
            func.date(Document.created_at).label("day"),
            func.count(Document.id)
        )
        .filter(Document.created_at >= start_date)
        .group_by("day")
        .order_by("day")
        .all()
    )

    uploads_map = {
        str(day): count
        for day, count in uploads_raw
        if day is not None
    }

    uploads_per_day = []
    for i in range(10):
        d = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        uploads_per_day.append((d, uploads_map.get(d, 0)))

    # ------------------------------
    # FILE TYPE DISTRIBUTION
    # ------------------------------
    raw_types = (
        doc_query
        .with_entities(Document.file_type, func.count(Document.id))
        .group_by(Document.file_type)
        .all()
    )

    normalized = {}
    for ftype, cnt in raw_types:
        clean = (ftype or "other").strip().lower() or "other"
        normalized[clean] = cnt

    type_distribution = [
        (ext, normalized.get(ext, 0))
        for ext in FILE_TYPE_ORDER
        if normalized.get(ext, 0) > 0
    ]

    if not type_distribution:
        type_distribution = [("other", 1)]

    # ------------------------------
    # NOTIFICATIONS
    # ------------------------------
    if current_user.is_admin:
        unread_notifications = (
            Notification.query
            .filter_by(is_read=False)
            .order_by(Notification.created_at.desc())
            .all()
        )
    else:
        unread_notifications = (
            Notification.query
            .filter_by(
                is_read=False,
                user_id=current_user.id
            )
            .order_by(Notification.created_at.desc())
            .all()
        )

    # ------------------------------
    # RENDER
    # ------------------------------
    return render_template(
        "dashboard/index.html",
        total_docs=total_docs,
        active_docs=active_docs,
        archived_docs=archived_docs,
        total_users=total_users,
        total_folders=total_folders,
        uploads_week=uploads_week,
        recent_docs=recent_docs,
        recent_folders=recent_folders,
        recent_activities=recent_activities,
        uploads_per_day=uploads_per_day,
        type_distribution=type_distribution,
        expiring_docs=expiring_docs,
        unread_notifications=unread_notifications,
    )
