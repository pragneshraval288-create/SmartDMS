import os
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..models import Document

storage_bp = Blueprint("storage", __name__, url_prefix="/storage")


@storage_bp.route("/")
@login_required
def index():

    # ==================================================
    # ADMIN VIEW → SYSTEM STORAGE
    # ==================================================
    if current_user.is_admin:
        storage_path = os.path.abspath("storage/files")

        total_files = 0
        total_size = 0

        if os.path.exists(storage_path):
            for root, _, files in os.walk(storage_path):
                for f in files:
                    total_files += 1
                    try:
                        total_size += os.path.getsize(os.path.join(root, f))
                    except OSError:
                        pass

        stats = [
            {"label": "Total Files (System)", "value": total_files},
            {
                "label": "Total Size (System)",
                "value": f"{round(total_size / (1024 * 1024), 2)} MB"
            },
            {"label": "Storage Path", "value": storage_path},
        ]

        return render_template(
            "storage/index.html",
            stats=stats
        )

    # ==================================================
    # USER VIEW → OWN DOCUMENT STORAGE
    # ==================================================
    user_docs = Document.query.filter_by(
        uploaded_by=current_user.id,
        is_deleted=False
    ).all()

    user_files = 0
    user_size = 0

    for doc in user_docs:
        if doc.filepath and os.path.exists(doc.filepath):
            user_files += 1
            try:
                user_size += os.path.getsize(doc.filepath)
            except OSError:
                pass

    stats = [
        {"label": "Your Documents", "value": user_files},
        {
            "label": "Your Storage Usage",
            "value": f"{round(user_size / (1024 * 1024), 2)} MB"
        }
    ]

    return render_template(
        "storage/index.html",
        stats=stats
    )
