import os
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from backend.extensions import db
from backend.models.models import Document, Audit
from backend.forms.document_forms import DocumentForm

bp = Blueprint('documents', __name__)

# ✅ File validation setup
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ✅ Helper: Save uploaded file
def save_file(file, version: int) -> str:
    """Save file with versioned, unique name like name_v1.pdf, name_v2.pdf, etc."""
    original_name = secure_filename(file.filename)
    name, ext = os.path.splitext(original_name)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    filename = f"{name}_v{version}{ext}"
    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)
    return filename

# ✅ Helper: Get next version number for this filename (grouped by original name)
def next_version_for_filename(filename: str) -> int:
    """Return next version number based on existing stored filenames.

    We derive base name and extension from the uploaded filename and then
    look for stored filenames like "name_v1.ext", "name_v2.ext", etc.
    """
    original_name = secure_filename(filename)
    base, ext = os.path.splitext(original_name)
    pattern = f"{base}_v%{ext}"
    latest = (
        Document.query.filter(Document.filename.ilike(pattern))
        .order_by(Document.version.desc())
        .first()
    )
    return latest.version + 1 if latest else 1

# ✅ Ownership check
def _owns(doc):
    return (current_user.role == "admin") or (current_user.id == doc.uploader_id)

# ✅ List documents
@bp.route('/documents')
@login_required
def list():
    page = int(request.args.get('page', 1))
    per_page = 10

    q = Document.query if current_user.role == "admin" else Document.query.filter_by(uploader_id=current_user.id)

    title = request.args.get('title')
    tags  = request.args.get('tags')
    ftype = request.args.get('type')

    if title:
        q = q.filter(Document.title.ilike(f'%{title}%'))
    if tags:
        q = q.filter(Document.tags.ilike(f'%{tags}%'))

    if ftype:
        if ftype == "image":
            q = q.filter(
                Document.filename.ilike('%.jpg') |
                Document.filename.ilike('%.jpeg') |
                Document.filename.ilike('%.png')
            )
        else:
            q = q.filter(Document.filename.ilike(f'%.{ftype}'))

    total_pages = (q.count() // per_page) + (1 if q.count() % per_page > 0 else 0)

    docs = (
        q.order_by(Document.upload_date.desc())
         .offset((page - 1) * per_page)
         .limit(per_page)
         .all()
    )

    return render_template("documents.html", documents=docs, page=page, total_pages=total_pages)

# ✅ Upload documents
@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = DocumentForm()

    if form.validate_on_submit() and form.file.data:
        file = form.file.data
        if not allowed_file(file.filename):
            flash("File type not allowed!", "danger")
            return redirect(request.url)

        version = next_version_for_filename(file.filename)  # ✅ fixed version call
        stored_filename = save_file(file, version)

        doc = Document(
            title=form.title.data,
            filename=stored_filename,
            uploader_id=current_user.id,
            tags=form.tags.data,
            version=version,
            upload_date=datetime.utcnow(),
        )

        db.session.add(doc)
        db.session.commit()

        audit = Audit(
            user_id=current_user.id,
            action="Uploaded document",
            filename=stored_filename,
            version=version,
            timestamp=datetime.utcnow(),
            user=current_user
        )

        db.session.add(audit)
        db.session.commit()

        flash("File uploaded successfully!", "success")
        return redirect(url_for("documents.list"))

    return render_template("upload.html", form=form, edit_mode=True)

# ✅ Preview
@bp.route('/preview/<int:doc_id>')
@login_required
def preview(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if not _owns(doc):
        flash("Permission denied!", "danger")
        return redirect(url_for("documents.list"))

    return send_from_directory(current_app.config["UPLOAD_FOLDER"], doc.filename, as_attachment=False)

# ✅ Download + audit
@bp.route('/download/<int:doc_id>')
@login_required
def download(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if not _owns(doc):
        flash("Permission denied!", "danger")
        return redirect(url_for("documents.list"))

    audit = Audit(
        user_id=current_user.id,
        action="Downloaded document",
        filename=doc.filename,
        version=doc.version,
        timestamp=datetime.utcnow(),
        user=current_user
    )
    db.session.add(audit)
    db.session.commit()

    return send_from_directory(current_app.config["UPLOAD_FOLDER"], doc.filename, as_attachment=True)

# ✅ Update metadata + optional new version
@bp.route('/update/<int:doc_id>', methods=['GET', 'POST'])
@login_required
def update(doc_id):
    original = Document.query.get_or_404(doc_id)
    if not _owns(original):
        flash("Permission denied!", "danger")
        return redirect(url_for("documents.list"))

    form = DocumentForm()

    if form.validate_on_submit():
        original.title = form.title.data
        original.tags  = form.tags.data
        db.session.commit()

        if form.file.data:
            file = form.file.data
            if not allowed_file(file.filename):
                flash("File type not allowed for new version!", "danger")
                return redirect(request.url)

            version = next_version_for_filename(file.filename)
            new_filename = save_file(file, version)

            new_doc = Document(
                title=original.title,
                filename=new_filename,
                uploader_id=original.uploader_id,
                tags=original.tags,
                version=version,
                upload_date=datetime.utcnow(),
            )

            db.session.add(new_doc)
            db.session.commit()

            audit = Audit(
                user_id=current_user.id,
                action="Updated document, created new version",
                filename=new_doc.filename,
                version=new_doc.version,
                timestamp=datetime.utcnow(),
                user=current_user
            )
            db.session.add(audit)
            db.session.commit()

            flash("New version created!", "success")

        flash("Document updated!", "success")
        return redirect(url_for("documents.list"))

    if request.method == "GET":
        form.title.data = original.title
        form.tags.data  = original.tags

    return render_template("update_document.html", form=form, doc=original)

# ✅ FIXED delete route
@bp.route('/delete/<int:doc_id>')
@login_required
def delete(doc_id):
    doc = Document.query.get_or_404(doc_id)  # ✅ fixed
    if not _owns(doc):
        flash("Permission denied!", "danger")
        return redirect(url_for("documents.list"))

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], doc.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    version = doc.version
    filename = doc.filename

    db.session.delete(doc)
    db.session.commit()

    audit = Audit(
        user_id=current_user.id,
        action="Deleted document",
        filename=filename,
        version=version,
        timestamp=datetime.utcnow(),
        user=current_user
    )
    db.session.add(audit)
    db.session.commit()

    flash("Document deleted!", "success")
    return redirect(url_for("documents.list"))
