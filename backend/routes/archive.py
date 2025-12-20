from flask import Blueprint, render_template
from flask_login import login_required
from ..models import Document

archive_bp = Blueprint("archive", __name__, url_prefix="/archive")


@archive_bp.route("/")
@login_required
def index():
    documents = (
        Document.query
        .filter_by(is_active=False)
        .order_by(Document.updated_at.desc())
        .all()
    )

    return render_template(
        "archive/index.html",
        documents=documents
    )
