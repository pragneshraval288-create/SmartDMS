from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import DocumentShare, Document

sharing_bp = Blueprint("sharing", __name__, url_prefix="/sharing")


@sharing_bp.route("/")
@login_required
def index():
    shared_docs = (
        Document.query
        .join(DocumentShare, Document.id == DocumentShare.document_id)
        .filter(DocumentShare.shared_with_id == current_user.id)
        .all()
    )

    return render_template(
        "sharing/index.html",
        documents=shared_docs
    )
