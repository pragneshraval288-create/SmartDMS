from backend.extensions import db
from backend.models.models import Audit
from flask_login import current_user
from datetime import datetime

def log_audit(action, filename, version):
    log = Audit(
        user_id=current_user.id,
        action=action,
        filename=filename,
        version=version,
        timestamp=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()
