from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..models import Document
from ..extensions import db

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/documents")
@login_required
def api_documents():
    docs = Document.query.limit(50).all()
    data = [
        {
            "id": d.id,
            "title": d.title,
            "category": d.category,
            "file_type": d.file_type,
            "version": d.version,
            "status": d.status,
            "is_active": d.is_active,
            "uploaded_by": d.uploader.username if d.uploader else None,
            "created_at": d.created_at.isoformat(),
        }
        for d in docs
    ]
    return jsonify(data)
