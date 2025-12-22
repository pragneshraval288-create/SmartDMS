from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Document, Folder
from ..services.activity_service import log_activity

recycle_bin_bp = Blueprint(
    "recycle_bin",
    __name__,
    url_prefix="/recycle-bin"
)

# =====================================================
# 🔥 HELPERS (RECURSIVE & SAFE)
# =====================================================
def _restore_folder_recursive(folder: Folder):
    folder.is_deleted = False
    folder.deleted_at = None

    # restore documents
    for doc in folder.documents:
        doc.is_deleted = False
        doc.deleted_at = None

    # restore subfolders
    for child in folder.children:
        _restore_folder_recursive(child)


def _delete_folder_recursive(folder: Folder):
    # delete documents first
    for doc in folder.documents:
        db.session.delete(doc)

    # delete child folders
    for child in folder.children:
        _delete_folder_recursive(child)

    # finally delete this folder
    db.session.delete(folder)


# =====================================================
# RECYCLE BIN HOME
# =====================================================
@recycle_bin_bp.route("/", methods=["GET"])
@login_required
def index():
    deleted_documents = (
        Document.query
        .filter(
            Document.uploaded_by == current_user.id,
            Document.is_deleted == True
        )
        .order_by(Document.deleted_at.desc())
        .all()
    )

    deleted_folders = (
        Folder.query
        .filter(
            Folder.created_by == current_user.id,
            Folder.is_deleted == True
        )
        .order_by(Folder.deleted_at.desc())
        .all()
    )

    return render_template(
        "recycle_bin/index.html",
        deleted_documents=deleted_documents,
        deleted_folders=deleted_folders
    )


# =====================================================
# RESTORE DOCUMENT
# =====================================================
@recycle_bin_bp.route("/document/<int:document_id>/restore", methods=["POST"])
@login_required
def restore_document(document_id):
    doc = Document.query.get_or_404(document_id)

    if doc.uploaded_by != current_user.id:
        abort(403)

    doc.is_deleted = False
    doc.deleted_at = None
    db.session.commit()

    log_activity(
        "document_restore",
        details=f"Restored document '{doc.title}'"
    )

    flash("Document restored successfully.", "success")
    return redirect(url_for("recycle_bin.index"))


# =====================================================
# PERMANENT DELETE DOCUMENT
# =====================================================
@recycle_bin_bp.route("/document/<int:document_id>/delete", methods=["POST"])
@login_required
def delete_document_permanently(document_id):
    doc = Document.query.get_or_404(document_id)

    if doc.uploaded_by != current_user.id:
        abort(403)

    db.session.delete(doc)
    db.session.commit()

    log_activity(
        "document_delete_permanent",
        details=f"Permanently deleted document '{doc.title}'"
    )

    flash("Document permanently deleted.", "danger")
    return redirect(url_for("recycle_bin.index"))


# =====================================================
# RESTORE FOLDER
# =====================================================
@recycle_bin_bp.route("/folder/<int:folder_id>/restore", methods=["POST"])
@login_required
def restore_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    if folder.created_by != current_user.id:
        abort(403)

    _restore_folder_recursive(folder)
    db.session.commit()

    log_activity(
        "folder_restore",
        details=f"Restored folder '{folder.name}'"
    )

    flash("Folder restored successfully.", "success")
    return redirect(url_for("recycle_bin.index"))


# =====================================================
# PERMANENT DELETE FOLDER
# =====================================================
@recycle_bin_bp.route("/folder/<int:folder_id>/delete", methods=["POST"])
@login_required
def delete_folder_permanently(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    if folder.created_by != current_user.id:
        abort(403)

    _delete_folder_recursive(folder)
    db.session.commit()

    log_activity(
        "folder_delete_permanent",
        details=f"Permanently deleted folder '{folder.name}'"
    )

    flash("Folder permanently deleted.", "danger")
    return redirect(url_for("recycle_bin.index"))


# =====================================================
# EMPTY RECYCLE BIN
# =====================================================
@recycle_bin_bp.route("/empty", methods=["POST"])
@login_required
def empty_recycle_bin():

    # delete documents
    Document.query.filter(
        Document.uploaded_by == current_user.id,
        Document.is_deleted == True
    ).delete(synchronize_session=False)

    # delete folders recursively
    folders = Folder.query.filter(
        Folder.created_by == current_user.id,
        Folder.is_deleted == True
    ).all()

    for folder in folders:
        _delete_folder_recursive(folder)

    db.session.commit()

    log_activity(
        "recycle_bin_empty",
        details="Emptied recycle bin"
    )

    flash("Recycle Bin emptied successfully.", "danger")
    return redirect(url_for("recycle_bin.index"))
