import os
from flask import Blueprint, render_template
from flask_login import login_required, current_user

storage_bp = Blueprint("storage", __name__, url_prefix="/storage")


@storage_bp.route("/")
@login_required
def index():
    # FINAL: only admin/manager can view storage stats
    if not (current_user.is_admin or current_user.is_manager):
        return render_template("storage/index.html", stats=[])

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
        {"label": "Total Files", "value": total_files},
        {"label": "Total Size", "value": f"{round(total_size / (1024 * 1024), 2)} MB"},
        {"label": "Storage Path", "value": storage_path},
    ]

    return render_template(
        "storage/index.html",
        stats=stats
    )
