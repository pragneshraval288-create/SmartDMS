from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from ..models import Document

bp = Blueprint('api', __name__)

@bp.route('/api/documents')
@login_required
def documents_api():
    q = Document.query if current_user.role=='admin' else Document.query.filter_by(uploader_id=current_user.id)
    q = q.order_by(Document.upload_date.desc()).all()
    return jsonify([{
        'id': d.id, 'title': d.title, 'filename': d.filename, 'uploader_id': d.uploader_id,
        'tags': d.tags, 'upload_date': d.upload_date.isoformat(), 'version': d.version
    } for d in q])
