from flask import request
from flask_login import current_user
from ..extensions import db
from ..models import ActivityLog


def log_activity(action, document_id=None, details=None):
    log = ActivityLog(
        action=action,
        user_id=current_user.id if current_user.is_authenticated else None,
        document_id=document_id,
        details=details,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
