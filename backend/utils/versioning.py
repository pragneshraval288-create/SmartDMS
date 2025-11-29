from backend.models.models import Document

def next_version_for_filename(filename):
    base = filename.split('.')[0]
    latest = Document.query.filter(Document.filename.like(f"{base}%")).order_by(Document.version.desc()).first()
    return latest.version + 1 if latest else 1
