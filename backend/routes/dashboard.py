from datetime import datetime, timedelta
import logging
from flask import Blueprint, render_template, flash, current_app
from flask_login import login_required, current_user
from sqlalchemy import func, or_
from sqlalchemy.exc import SQLAlchemyError

from ..models import (
    Document,
    User,
    ActivityLog,
    Notification,
    Folder,
    DocumentShare
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)

# Constants
FILE_TYPE_ORDER = [
    "pdf", "doc", "docx", "xls", "xlsx",
    "ppt", "pptx", "txt", "png", "jpg",
    "jpeg", "zip", "other"
]

@dashboard_bp.route("/", methods=["GET"])
@login_required
def index():
    """
    Renders the main dashboard with statistics, graphs, and recent activities.
    Includes error handling to prevent crashes if DB queries fail.
    """
    
    # Initialize default values to prevent UnboundLocalError in case of exception
    total_docs = 0
    active_docs = 0
    archived_docs = 0
    total_users = 0
    total_folders = 0
    uploads_week = 0
    expiring_docs = []
    recent_docs = []
    recent_folders = []
    recent_activities = []
    uploads_per_day = []
    type_distribution = []
    unread_notifications = []

    try:
        # ==================================================
        # 1. BASE QUERIES (RBAC Enforced)
        # ==================================================
        # Define the scope of documents visible to the user
        if current_user.is_admin:
            doc_query = Document.query.filter(Document.is_deleted.is_(False))
            folder_query = Folder.query.filter(Folder.is_deleted.is_(False))
        else:
            # Employees see their own docs + shared docs
            doc_query = (
                Document.query
                .outerjoin(DocumentShare, Document.id == DocumentShare.document_id)
                .filter(
                    Document.is_deleted.is_(False),
                    or_(
                        Document.uploaded_by == current_user.id,
                        DocumentShare.shared_with_id == current_user.id
                    )
                )
                .distinct()
            )
            # Employees only see folders they created
            folder_query = Folder.query.filter(
                Folder.created_by == current_user.id,
                Folder.is_deleted.is_(False)
            )

        # ==================================================
        # 2. CALCULATE BASIC STATS
        # ==================================================
        total_docs = doc_query.count()
        active_docs = doc_query.filter(Document.is_active.is_(True)).count()
        archived_docs = doc_query.filter(Document.is_active.is_(False)).count()
        
        # Only admins might technically need total users, but showing to all is fine for dashboard
        total_users = User.query.count() 
        total_folders = folder_query.count()

        one_week_ago = datetime.utcnow() - timedelta(days=7)
        uploads_week = doc_query.filter(Document.created_at >= one_week_ago).count()

        # ==================================================
        # 3. CRITICAL ALERTS (Expiring Docs)
        # ==================================================
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

        # ==================================================
        # 4. RECENT ITEMS
        # ==================================================
        recent_docs = (
            doc_query
            .order_by(Document.created_at.desc())
            .limit(5)
            .all()
        )

        recent_folders = (
            folder_query
            .filter(Folder.parent_id.is_(None)) # Only root folders in recent view
            .order_by(Folder.created_at.desc())
            .limit(5)
            .all()
        )

        # ==================================================
        # 5. RECENT ACTIVITIES (Audit Logs)
        # ==================================================
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

        # ==================================================
        # 6. GRAPH DATA: UPLOAD TRENDS
        # ==================================================
        today = datetime.utcnow().date()
        start_date = today - timedelta(days=9)

        # Using func.date to group by day (DB agnostic usually, mostly SQLite/Postgres friendly)
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

        # Map results to dictionary for easy lookup
        uploads_map = {str(day): count for day, count in uploads_raw if day is not None}

        # Fill in missing days with 0
        for i in range(10):
            d = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            uploads_per_day.append((d, uploads_map.get(d, 0)))

        # ==================================================
        # 7. GRAPH DATA: FILE TYPES
        # ==================================================
        raw_types = (
            doc_query
            .with_entities(Document.file_type, func.count(Document.id))
            .group_by(Document.file_type)
            .all()
        )

        normalized = {}
        for ftype, cnt in raw_types:
            clean = (ftype or "other").strip().lower()
            if not clean: 
                clean = "other"
            normalized[clean] = normalized.get(clean, 0) + cnt

        # Sort according to predefined order
        for ext in FILE_TYPE_ORDER:
            if normalized.get(ext, 0) > 0:
                type_distribution.append((ext, normalized[ext]))
        
        # Add any types not in our order list to 'other' or append them
        known_types = set(FILE_TYPE_ORDER)
        for ext, count in normalized.items():
            if ext not in known_types:
                 # You might want to aggregate these into "other" or list them separately
                 pass 

        # Fallback for empty state
        if not type_distribution:
            type_distribution = [("other", 0)]

        # ==================================================
        # 8. NOTIFICATIONS
        # ==================================================
        notif_query = Notification.query.filter_by(is_read=False)
        if not current_user.is_admin:
            notif_query = notif_query.filter_by(user_id=current_user.id)
            
        unread_notifications = (
            notif_query
            .order_by(Notification.created_at.desc())
            .all()
        )

    except SQLAlchemyError as e:
        # Log the error (In production, use app.logger)
        print(f"Error loading dashboard: {str(e)}")
        current_app.logger.error(f"Dashboard Database Error: {e}")
        flash("Could not load some dashboard data due to a system error.", "danger")
    except Exception as e:
        print(f"Unexpected error in dashboard: {str(e)}")
        current_app.logger.error(f"Dashboard Generic Error: {e}")
        flash("An unexpected error occurred.", "warning")

    # ==================================================
    # RENDER TEMPLATE
    # ==================================================
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