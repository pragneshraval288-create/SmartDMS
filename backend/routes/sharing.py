from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import DocumentShare, Document
from ..extensions import db

sharing_bp = Blueprint("sharing", __name__, url_prefix="/sharing")

@sharing_bp.route("/")
@login_required
def index():
    # Fix 1: Convert User ID to Integer
    current_user_id = int(current_user.id)

    shared_docs = (
        Document.query
        .join(DocumentShare, Document.id == DocumentShare.document_id)
        .filter(DocumentShare.shared_with_id == current_user_id)
        # Fix 2: Ensure we don't show deleted documents (Trash Items)
        .filter(Document.is_deleted == False) 
        .all()
    )

    return render_template(
        "sharing/index.html",
        documents=shared_docs
    )