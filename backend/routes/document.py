# backend/routes/documents.py

from io import BytesIO
from werkzeug.datastructures import FileStorage
from datetime import datetime
from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, request, send_file, abort, jsonify
)
from flask_login import login_required, current_user
from sqlalchemy import or_

from ..extensions import db
from ..models import (
    Document, DocumentVersion, DocumentComment,
    DocumentShare, User, Folder
)
from ..forms import (
    CommentForm, ShareForm, UploadForm,
    DocumentFilterForm
)

from ..services.document_service import (
    create_document, update_document_file,
    soft_archive, restore, increment_download
)
from ..services.activity_service import log_activity
from ..services.notification_service import notify_user
from ..services.storage_service import decrypt_file, save_encrypted_file

document_bp = Blueprint("document", __name__, url_prefix="/documents")

# =========================
# HELPERS
# =========================
def _user_can_view(doc: Document) -> bool:
    if current_user.is_admin:
        return True
    if doc.uploaded_by == int(current_user.id):
        return True
    return DocumentShare.query.filter_by(
        document_id=doc.id,
        shared_with_id=int(current_user.id)
    ).first() is not None


def _user_owns_folder(folder_id):
    if not folder_id:
        return True
    folder = Folder.query.get(folder_id)
    if not folder:
        return False
    return current_user.is_admin or folder.created_by == int(current_user.id)


# ==================================================
# LIST DOCUMENTS + FOLDERS
# ==================================================
@document_bp.route("/", methods=["GET"])
@login_required
def list_documents():
    form = DocumentFilterForm(request.args)
    folder_id = request.args.get("folder", type=int)
    current_user_id = int(current_user.id)

    active_folder = None
    if folder_id:
        active_folder = Folder.query.get_or_404(folder_id)
        if not current_user.is_admin and active_folder.created_by != current_user_id:
            flash("Permission denied.", "danger")
            return redirect(url_for("document.list_documents"))

    # 1. Query Folders
    folder_query = Folder.query.filter(Folder.deleted_at.is_(None))
    if not current_user.is_admin:
        folder_query = folder_query.filter(Folder.created_by == current_user_id)

    if active_folder:
        folder_query = folder_query.filter(Folder.parent_id == active_folder.id)
    else:
        folder_query = folder_query.filter(Folder.parent_id.is_(None))

    folders = folder_query.order_by(Folder.created_at.asc()).all()

    # 2. Query Documents
    doc_query = Document.query.filter(Document.is_deleted.is_(False))

    if not current_user.is_admin:
        doc_query = doc_query.filter(
            or_(
                Document.uploaded_by == current_user_id,
                Document.id.in_(
                    db.session.query(DocumentShare.document_id)
                    .filter(DocumentShare.shared_with_id == current_user_id)
                )
            )
        )

    if active_folder:
        doc_query = doc_query.filter(Document.folder_id == active_folder.id)
    else:
        doc_query = doc_query.filter(Document.folder_id.is_(None))

    if form.search.data:
        like = f"%{form.search.data.strip()}%"
        doc_query = doc_query.filter(
            or_(Document.title.ilike(like), Document.tags.ilike(like))
        )

    status = form.status.data or "active"
    if status == "archived":
        doc_query = doc_query.filter(Document.is_active.is_(False))
    else:
        doc_query = doc_query.filter(Document.is_active.is_(True))

    documents = doc_query.order_by(Document.created_at.desc()).all()

    items = (
        [{"type": "folder", "obj": f} for f in folders] +
        [{"type": "document", "obj": d} for d in documents]
    )

    return render_template(
        "documents/list.html",
        items=items,
        active_folder=active_folder,
        form=form
    )


# =========================
# CREATE FOLDER
# =========================
@document_bp.route("/create_folder", methods=["POST"])
@login_required
def create_folder():
    name = request.form.get("name", "").strip()
    parent_id = request.form.get("parent_id", type=int)

    if not name:
        flash("Folder name is required.", "danger")
        return redirect(url_for("document.list_documents", folder=parent_id))

    if parent_id and not _user_owns_folder(parent_id):
        flash("Permission denied.", "danger")
        return redirect(url_for("document.list_documents"))

    new_folder = Folder(
        name=name,
        parent_id=parent_id,
        created_by=int(current_user.id)
    )
    db.session.add(new_folder)
    db.session.commit()

    log_activity("folder_create", details=f"Created folder '{name}'")
    flash("Folder created successfully.", "success")
    
    return redirect(url_for("document.list_documents", folder=parent_id))


# =========================
# MY DOCUMENTS
# =========================
@document_bp.route("/my")
@login_required
def my_documents():
    documents = (
        Document.query
        .filter_by(uploaded_by=int(current_user.id))
        .order_by(Document.created_at.desc())
        .all()
    )
    return render_template("documents/my_documents.html", documents=documents)


# =========================
# UPLOAD DOCUMENT
# =========================
@document_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    active_folder_id = request.args.get("folder", type=int)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        tags = request.form.get("tags", "").strip()
        folder_id = request.form.get("folder_id", type=int) or active_folder_id

        if folder_id and not _user_owns_folder(folder_id):
            flash("Invalid folder selected.", "danger")
            return redirect(request.url)

        files = request.files.getlist("files")
        if not title or not files:
            flash("Title and file required.", "danger")
            return redirect(request.url)

        for i, file in enumerate(files):
            if not file or file.filename == "":
                continue

            doc_title = title if i == 0 else f"{title} ({i + 1})"
            create_document(
                user=current_user,
                title=doc_title,
                tags=tags,
                file_storage=file,
                folder_id=folder_id,
                status="uploaded"
            )

        flash("Documents uploaded successfully.", "success")
        return redirect(url_for("document.list_documents", folder=folder_id) if folder_id else url_for("document.list_documents"))

    return render_template("documents/upload.html", form=UploadForm(), active_folder=active_folder_id)


# =========================
# MOVE DOCUMENT
# =========================
@document_bp.route("/<int:doc_id>/move", methods=["POST"])
@login_required
def move_document(doc_id):
    data = request.get_json(silent=True) or {}
    target_folder_id = data.get("parent_id")

    doc = Document.query.get_or_404(doc_id)

    if not _user_can_view(doc):
        return jsonify(success=False, error="Permission denied"), 403

    if doc.folder_id == target_folder_id:
        return jsonify(success=False, error="Document already in this folder"), 400

    if target_folder_id and not _user_owns_folder(target_folder_id):
        return jsonify(success=False, error="Cannot move to a folder you do not own"), 403

    doc.folder_id = target_folder_id
    db.session.commit()

    log_activity(
        action="document_move",
        document_id=doc.id,
        details=f"Moved document '{doc.title}'"
    )

    return jsonify(success=True)


# =========================
# COPY DOCUMENT
# =========================
@document_bp.route("/<int:doc_id>/copy", methods=["POST"])
@login_required
def copy_document(doc_id):
    data = request.get_json(silent=True) or {}
    target_folder_id = data.get("parent_id")

    doc = Document.query.get_or_404(doc_id)

    if not _user_can_view(doc):
        return jsonify(success=False, error="Permission denied"), 403

    if target_folder_id and not _user_owns_folder(target_folder_id):
        return jsonify(success=False, error="Cannot copy to a folder you do not own"), 403

    try:
        # decrypt original file
        file_bytes = decrypt_file(doc.filepath)

        # bytes -> FileStorage
        copied_file = FileStorage(
            stream=BytesIO(file_bytes),
            filename=doc.filename,
            content_type="application/octet-stream"
        )

        # save encrypted copy
        stored_path, stored_name = save_encrypted_file(copied_file)

        new_doc = Document(
            title=doc.title,
            tags=doc.tags,
            filename=doc.filename,
            stored_name=stored_name,
            filepath=stored_path,
            file_type=doc.file_type,
            uploaded_by=int(current_user.id),
            folder_id=target_folder_id,
            version=1,
            is_active=True
        )

        db.session.add(new_doc)
        db.session.commit()

        log_activity(
            action="document_copy",
            document_id=new_doc.id,
            details=f"Copied document '{doc.title}'"
        )

        return jsonify(success=True)

    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, error=str(e)), 500


# =========================
# DOCUMENT DETAIL
# =========================
@document_bp.route("/<int:document_id>", methods=["GET", "POST"])
@login_required
def detail(document_id):
    doc = Document.query.get_or_404(document_id)
    if not _user_can_view(doc):
        abort(403)

    comment_form = CommentForm()
    share_form = ShareForm()

    if comment_form.validate_on_submit():
        comment = DocumentComment(
            document_id=doc.id,
            user_id=int(current_user.id),
            content=comment_form.content.data.strip()
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment added.", "success")
        return redirect(url_for("document.detail", document_id=doc.id))

    versions = DocumentVersion.query.filter_by(document_id=doc.id).order_by(DocumentVersion.version.desc()).all()
    comments = DocumentComment.query.filter_by(document_id=doc.id).order_by(DocumentComment.created_at.desc()).all()
    shares = DocumentShare.query.filter_by(document_id=doc.id).all()

    return render_template(
        "documents/detail.html",
        document=doc,
        versions=versions,
        comments=comments,
        shares=shares,
        comment_form=comment_form,
        share_form=share_form
    )


# =========================
# DOWNLOAD / PREVIEW
# =========================
@document_bp.route("/<int:document_id>/download")
@login_required
def download(document_id):
    doc = Document.query.get_or_404(document_id)
    if not _user_can_view(doc):
        abort(403)

    data = decrypt_file(doc.filepath)
    increment_download(doc)

    return send_file(
        BytesIO(data),
        as_attachment=True,
        download_name=doc.filename
    )


@document_bp.route("/<int:document_id>/preview")
@login_required
def preview(document_id):
    doc = Document.query.get_or_404(document_id)
    if not _user_can_view(doc):
        abort(403)

    if doc.file_type not in ("pdf", "png", "jpg", "jpeg"):
        flash("Preview not available for this file type.", "info")
        return redirect(url_for("document.detail", document_id=doc.id))

    data = decrypt_file(doc.filepath)
    
    # Explicit MIME types prevent sniffing attacks
    mime = "application/pdf" if doc.file_type == "pdf" else f"image/{'jpeg' if doc.file_type in ('jpg','jpeg') else 'png'}"

    return send_file(BytesIO(data), mimetype=mime)


# =========================
# UPDATE FILE (NEW VERSION)
# =========================
@document_bp.route("/<int:document_id>/update_file", methods=["POST"])
@login_required
def update_file(document_id):
    doc = Document.query.get_or_404(document_id)

    if doc.uploaded_by != int(current_user.id) and not current_user.is_admin:
        flash("You are not allowed to update this document.", "danger")
        return redirect(url_for("document.detail", document_id=document_id))

    file = request.files.get("file")
    if not file or file.filename == "":
        flash("Please choose a file.", "danger")
        return redirect(url_for("document.detail", document_id=document_id))

    update_document_file(doc, file)
    flash("New version uploaded.", "success")
    return redirect(url_for("document.detail", document_id=document_id))

# =========================
# ARCHIVE / RESTORE
# =========================
@document_bp.route("/<int:document_id>/archive", methods=["POST"])
@login_required
def archive(document_id):
    doc = Document.query.get_or_404(document_id)

    if doc.uploaded_by != int(current_user.id) and not current_user.is_admin:
        return jsonify(success=False, error="Permission denied"), 403

    soft_archive(doc)
    return jsonify(success=True)


@document_bp.route("/<int:document_id>/restore", methods=["POST"])
@login_required
def restore_view(document_id):
    if not current_user.is_admin:
        flash("Only admin can restore documents.", "danger")
        return redirect(url_for("archive.index"))

    doc = Document.query.get_or_404(document_id)
    restore(doc)
    flash("Document restored.", "success")
    return redirect(url_for("archive.index"))



# =========================
# SHARE DOCUMENT
# =========================
@document_bp.route("/<int:document_id>/share", methods=["POST"])
@login_required
def share(document_id):
    doc = Document.query.get_or_404(document_id)

    if doc.uploaded_by != int(current_user.id) and not current_user.is_admin:
        flash("You are not allowed to share this document.", "danger")
        return redirect(url_for("document.detail", document_id=document_id))

    form = ShareForm()
    if not form.validate_on_submit():
        flash("Invalid share request.", "danger")
        return redirect(url_for("document.detail", document_id=document_id))

    identifier = form.username_or_email.data.strip()
    user = User.query.filter(or_(User.username == identifier, User.email == identifier)).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("document.detail", document_id=document_id))

    existing = DocumentShare.query.filter_by(document_id=doc.id, shared_with_id=user.id).first()
    if existing:
        flash("Document already shared.", "warning")
        return redirect(url_for("document.detail", document_id=document_id))

    share = DocumentShare(document_id=doc.id, shared_with_id=user.id, can_edit=form.can_edit.data)
    db.session.add(share)
    db.session.commit()

    log_activity(
        action="share",
        document_id=doc.id,
        details=f"Shared with {user.username}"
    )

    notify_user(user, f"A document '{doc.title}' has been shared with you.")

    flash("Document shared successfully.", "success")
    return redirect(url_for("document.detail", document_id=document_id))


# =========================
# STATUS UPDATE (MANUAL)
# =========================
@document_bp.route("/<int:document_id>/status", methods=["POST"])
@login_required
def update_status(document_id):
    if not (current_user.is_manager or current_user.is_admin):
        abort(403)

    doc = Document.query.get_or_404(document_id)
    status = request.form.get("status")

    if status not in ("uploaded", "pending", "approved", "rejected"):
        flash("Invalid status.", "danger")
        return redirect(url_for("document.detail", document_id=document_id))

    doc.status = status
    db.session.commit()

    log_activity(
        "status_change",
        document_id=doc.id,
        details=f"Status changed to {status}"
    )

    notify_user(
        doc.uploader,
        f"Status of '{doc.title}' changed to {status}."
    )

    flash("Status updated.", "success")
    return redirect(url_for("document.detail", document_id=document_id))


# =========================
# GENERIC DELETE ITEM (Updated for Shares & Bulk)
# =========================
@document_bp.route("/delete_item", methods=["POST"])
@login_required
def delete_item():
    """
    Unified endpoint to Soft Delete either a Folder or a Document.
    Handles shared item removal ("Unshare") correctly.
    """
    item_type = request.form.get("item_type")
    item_id = request.form.get("item_id", type=int)
    current_user_id = int(current_user.id)

    if item_type == "folder":
        folder = Folder.query.get_or_404(item_id)
        if not current_user.is_admin and folder.created_by != current_user_id:
            flash("Permission denied.", "danger")
            return redirect(url_for("document.list_documents"))
        
        folder.deleted_at = datetime.utcnow()
        db.session.commit()
        log_activity("folder_delete", details=f"Soft deleted folder '{folder.name}'")
        flash("Folder deleted.", "success")
        return redirect(url_for("document.list_documents", folder=folder.parent_id))

    elif item_type == "document":
        doc = Document.query.get_or_404(item_id)
        
        # 1. If Owner -> Soft Delete
        if doc.uploaded_by == current_user_id or current_user.is_admin:
            doc.is_deleted = True
            doc.deleted_at = datetime.utcnow()
            db.session.commit()
            log_activity("document_bin", document_id=doc.id, details=f"Moved '{doc.title}' to recycle bin")
            flash("Document moved to recycle bin.", "success")
        
        # 2. If Shared Recipient -> Unshare (Permanently remove from view)
        else:
            share = DocumentShare.query.filter_by(
                document_id=doc.id,
                shared_with_id=current_user_id
            ).first()
            if share:
                db.session.delete(share)
                db.session.commit()
                log_activity("share_remove", document_id=doc.id, details=f"Removed shared document '{doc.title}'")
                flash("Shared document removed.", "success")
            else:
                flash("Permission denied.", "danger")

        return redirect(url_for("document.list_documents", folder=doc.folder_id))

    else:
        flash("Invalid item type.", "danger")
        return redirect(url_for("document.list_documents"))


# =========================
# SPECIFIC MOVE TO BIN (API) - Updated for Shares
# =========================
@document_bp.route("/<int:document_id>/bin", methods=["POST"])
@login_required
def move_document_to_bin(document_id):
    doc = Document.query.get_or_404(document_id)
    current_user_id = int(current_user.id)

    # 1. If Owner -> Soft Delete
    if doc.uploaded_by == current_user_id or current_user.is_admin:
        doc.is_deleted = True
        doc.deleted_at = datetime.utcnow()
        db.session.commit()
        log_activity("document_bin", document_id=doc.id, details=f"Moved '{doc.title}' to recycle bin")
        return jsonify(success=True)

    # 2. If Shared Recipient -> Unshare (Success)
    # Deleting the share link means it disappears from the recipient's list
    share = DocumentShare.query.filter_by(
        document_id=doc.id,
        shared_with_id=current_user_id
    ).first()

    if share:
        db.session.delete(share)
        db.session.commit()
        log_activity("share_remove", document_id=doc.id, details=f"Removed shared document '{doc.title}'")
        return jsonify(success=True)

    return jsonify(success=False, error="Permission denied. You do not own this document."), 403


# =========================
# PERMANENT DELETE DOCUMENT
# =========================
@document_bp.route("/<int:document_id>/delete", methods=["POST"])
@login_required
def delete_document(document_id):
    doc = Document.query.get_or_404(document_id)
    current_user_id = int(current_user.id)

    # Only owner/admin can permanently delete the FILE
    if doc.uploaded_by != current_user_id and not current_user.is_admin:
        return jsonify(success=False, error="Permission denied. Only the owner can permanently delete this."), 403

    doc_title = doc.title
    db.session.delete(doc)
    db.session.commit()

    log_activity(
        action="document_permanent_delete",
        document_id=None,
        details=f"Permanently deleted document '{doc_title}'"
    )

    return jsonify(success=True)


# =========================
# BULK MOVE DOCUMENTS TO RECYCLE BIN (Updated for Shares)
# =========================
@document_bp.route("/bulk/bin", methods=["POST"])
@login_required
def bulk_documents_move_to_bin():
    data = request.get_json(silent=True) or {}
    ids = data.get("ids", [])
    current_user_id = int(current_user.id)

    if not isinstance(ids, list):
        return jsonify(success=False, error="Invalid payload"), 400

    documents = Document.query.filter(Document.id.in_(ids)).all()

    for doc in documents:
        # Case 1: Owner -> Soft Delete
        if doc.uploaded_by == current_user_id or current_user.is_admin:
            doc.is_deleted = True
            doc.deleted_at = datetime.utcnow()
            log_activity("document_bin", document_id=doc.id, details=f"Moved '{doc.title}' to recycle bin")
        
        # Case 2: Shared Recipient -> Unshare
        else:
            share = DocumentShare.query.filter_by(document_id=doc.id, shared_with_id=current_user_id).first()
            if share:
                db.session.delete(share)
                log_activity("share_remove", document_id=doc.id, details=f"Removed shared document '{doc.title}'")

    db.session.commit()
    return jsonify(success=True)


# =========================
# BULK PERMANENT DELETE DOCUMENTS
# =========================
@document_bp.route("/bulk/delete", methods=["POST"])
@login_required
def bulk_documents_delete():
    data = request.get_json(silent=True) or {}
    ids = data.get("ids", [])
    current_user_id = int(current_user.id)

    if not isinstance(ids, list):
        return jsonify(success=False, error="Invalid payload"), 400

    documents = Document.query.filter(Document.id.in_(ids)).all()

    for doc in documents:
        # Only Owner can hard delete
        if doc.uploaded_by != current_user_id and not current_user.is_admin:
            continue

        doc_title = doc.title
        db.session.delete(doc)
        log_activity("document_permanent_delete", document_id=None, details=f"Permanently deleted document '{doc_title}'")

    db.session.commit()
    return jsonify(success=True)