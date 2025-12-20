from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import Document

favorites_bp = Blueprint("favorites", __name__, url_prefix="/favorites")


@favorites_bp.route("/")
@login_required
def index():
    """
    Favorites placeholder using user's uploaded documents.
    DOES NOT assume owner_id or favorites table.
    """

    documents = (
        Document.query
        .filter_by(uploaded_by=current_user.id)
        .order_by(Document.created_at.desc())
        .all()
    )

    return render_template(
        "favorites/index.html",
        documents=documents
    )
