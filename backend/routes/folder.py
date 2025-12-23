# backend/routes/folder.py

from flask import (
    Blueprint, request, jsonify,
    redirect, url_for, flash
)
import json
from datetime import datetime
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Folder, Document
from ..services.activity_service import log_activity

folder_bp = Blueprint(
    "folder",
    __name__,
    url_prefix="/documents/folders"
)

# =========================
# HELPERS
# =========================
def _owns_folder(folder: Folder) -> bool:
    return current_user.is_admin or folder.created_by == current_user.id


def _is_descendant(folder: Folder, target: Folder) -> bool:
    if not target or not target.parent_id:
        return False
    if target.parent_id == folder.id:
        return True
    return _is_descendant(folder, target.parent)


def _clone_folder(folder, parent_id=None):
    new_folder = Folder(
        name=f"{folder.name} (copy)",
        created_by=current_user.id,
        parent_id=parent_id
    )
    db.session.add(new_folder)
    db.session.flush()

    for doc in folder.documents:
        new_doc = Document(
            title=doc.title,
            filename=doc.filename,
            file_type=doc.file_type,
            tags=doc.tags,
            uploaded_by=doc.uploaded_by,
            folder_id=new_folder.id,
            is_active=doc.is_active
        )
        db.session.add(new_doc)

    for child in folder.children:
        _clone_folder(child, new_folder.id)

    return new_folder

def _hard_delete_folder(folder: Folder):
    # delete all documents inside folder
    for doc in folder.documents:
        db.session.delete(doc)

    # recursively delete child folders
    for child in folder.children:
        _hard_delete_folder(child)

    # finally delete the folder itself
    db.session.delete(folder)

# =========================
# CREATE FOLDER (PASTE TARGET)
# =========================
@folder_bp.route("/create", methods=["POST"])
@login_required
def create_folder():
    name = request.form.get("name", "").strip()
    parent_id = request.form.get("parent_id", type=int)

    if not name:
        flash("Folder name is required", "danger")
        return redirect(request.referrer)

    parent = Folder.query.get(parent_id) if parent_id else None

    if parent and not _owns_folder(parent):
        flash("Permission denied", "danger")
        return redirect(request.referrer)

    folder = Folder(
        name=name,
        created_by=current_user.id,
        parent_id=parent.id if parent else None
    )

    db.session.add(folder)
    db.session.commit()

    return redirect(request.referrer or url_for("dashboard.index"))



# =========================
# RENAME FOLDER
# =========================
@folder_bp.route("/<int:folder_id>/rename", methods=["POST"])
@login_required
def rename_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    if not _owns_folder(folder):
        return jsonify(success=False, error="Permission denied"), 403

    data = request.get_json(silent=True) or {}
    new_name = data.get("name", "").strip()

    if not new_name:
        return jsonify(success=False, error="Folder name required")

    exists = Folder.query.filter_by(
        name=new_name,
        parent_id=folder.parent_id,
        created_by=current_user.id
    ).first()

    if exists:
        return jsonify(success=False, error="Folder already exists")

    folder.name = new_name
    db.session.commit()

    log_activity(
        "folder_rename",
        details=f"Renamed folder to '{new_name}'"
    )

    return jsonify(success=True)


# =========================
# MOVE FOLDER (CUT + PASTE)
# =========================
@folder_bp.route("/<int:folder_id>/move", methods=["POST"])
@login_required
def move_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    if not _owns_folder(folder):
        return jsonify(success=False, error="Permission denied"), 403

    data = request.get_json(silent=True) or {}
    target_parent_id = data.get("parent_id")

    if target_parent_id == folder.id:
        return jsonify(success=False, error="Invalid target"), 400

    target = Folder.query.get(target_parent_id) if target_parent_id else None

    if target and not _owns_folder(target):
        return jsonify(success=False, error="Invalid target"), 403

    if target and _is_descendant(folder, target):
        return jsonify(
            success=False,
            error="Cannot move folder into its own subfolder"
        ), 400

    folder.parent_id = target_parent_id
    db.session.commit()

    log_activity(
        "folder_move",
        details=f"Moved folder '{folder.name}'"
    )

    return jsonify(success=True)


# =========================
# COPY FOLDER (COPY + PASTE)
# =========================
@folder_bp.route("/<int:folder_id>/copy", methods=["POST"])
@login_required
def copy_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    if not _owns_folder(folder):
        return jsonify(success=False, error="Permission denied"), 403

    data = request.get_json(silent=True) or {}
    target_parent_id = data.get("parent_id")

    target = Folder.query.get(target_parent_id) if target_parent_id else None

    if target and not _owns_folder(target):
        return jsonify(success=False, error="Invalid target"), 403

    _clone_folder(folder, target_parent_id)
    db.session.commit()

    log_activity(
        "folder_copy",
        details=f"Copied folder '{folder.name}'"
    )

    return jsonify(success=True)

# =========================
# FOLDER CONTENTS
# =========================
@folder_bp.route("/<int:folder_id>/contents")
@login_required
def folder_contents(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    if not (current_user.is_admin or folder.created_by == current_user.id):
        return jsonify(success=False), 403

    documents = [
        {
            "id": d.id,
            "title": d.title,
            "type": d.file_type,
            "created_at": d.created_at.strftime("%Y-%m-%d")
        }
        for d in folder.documents
    ]

    return jsonify(
        folder={"id": folder.id, "name": folder.name},
        documents=documents
    )


# =========================
# MOVE FOLDER TO RECYCLE BIN
# =========================
@folder_bp.route("/<int:folder_id>/bin", methods=["POST"])
@login_required
def move_folder_to_bin(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    if not _owns_folder(folder):
        return jsonify(success=False, error="Permission denied"), 403

    def _soft_delete_folder(f):
        f.is_deleted = True
        f.deleted_at = datetime.utcnow()

        for d in f.documents:
            d.is_deleted = True
            d.deleted_at = datetime.utcnow()

        for child in f.children:
            _soft_delete_folder(child)

    _soft_delete_folder(folder)
    db.session.commit()

    log_activity(
        "folder_bin",
        details=f"Moved folder '{folder.name}' to recycle bin"
    )

    return jsonify(success=True)


# =========================
# DELETE FOLDER (PERMANENT)
# =========================
@folder_bp.route("/<int:folder_id>/delete", methods=["POST"])
@login_required
def delete_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    if not _owns_folder(folder):
        return jsonify(success=False, error="Permission denied"), 403

    try:
        _hard_delete_folder(folder)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify(
            success=False,
            error=str(e)
        ), 500

    log_activity(
        "folder_permanent_delete",
        details=f"Permanently deleted folder '{folder.name}'"
    )

    return jsonify(success=True)


# =========================
# BULK MOVE FOLDERS TO RECYCLE BIN
# =========================
@folder_bp.route("/bulk/bin", methods=["POST"])
@login_required
def bulk_folder_move_to_bin():
    items = request.form.get("items")
    if not items:
        abort(400)

    data = json.loads(items)

    for item in data:
        if item["type"] != "folder":
            continue

        folder = Folder.query.get(item["id"])
        if not folder or not _owns_folder(folder):
            continue

        folder.is_deleted = True
        folder.deleted_at = datetime.utcnow()

        for doc in folder.documents:
            doc.is_deleted = True
            doc.deleted_at = datetime.utcnow()

    db.session.commit()
    flash("Selected folders moved to Recycle Bin.", "warning")
    return redirect(url_for("document.list_documents"))

# =========================
# BULK PERMANENT DELETE FOLDERS
# =========================
@folder_bp.route("/bulk/delete", methods=["POST"])
@login_required
def bulk_folder_delete():
    items = request.form.get("items")
    if not items:
        abort(400)

    data = json.loads(items)

    for item in data:
        if item["type"] != "folder":
            continue

        folder = Folder.query.get(item["id"])
        if not folder or not _owns_folder(folder):
            continue

        db.session.delete(folder)

    db.session.commit()
    flash("Selected folders permanently deleted.", "danger")
    return redirect(url_for("document.list_documents"))