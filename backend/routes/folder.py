# backend/routes/folder.py

from io import BytesIO
from flask import (
    Blueprint, request, jsonify,
    redirect, url_for, flash
)
from werkzeug.datastructures import FileStorage
from datetime import datetime
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Folder, Document
from ..services.activity_service import log_activity
from ..services.storage_service import decrypt_file, save_encrypted_file

folder_bp = Blueprint(
    "folder",
    __name__,
    url_prefix="/documents/folders"
)

# =========================
# HELPERS
# =========================

def _owns_folder(folder: Folder) -> bool:
    """Checks if current user owns the folder or is admin."""
    # FIX: Ensure int comparison so '2' == 2 works correctly
    return current_user.is_admin or folder.created_by == int(current_user.id)


def _is_descendant(folder: Folder, target: Folder) -> bool:
    """
    Prevents circular moves (e.g., moving a parent into its own child).
    Returns True if 'target' is inside 'folder' (recursively).
    """
    if not target or not target.parent_id:
        return False
    if target.parent_id == folder.id:
        return True
    return _is_descendant(folder, target.parent)


def _clone_folder(folder: Folder, parent_id=None):
    """
    Recursively clones a folder, its subfolders, and all documents.
    CRITICAL: It physically duplicates the encrypted files on disk.
    """
    current_user_id = int(current_user.id) # FIX: Use int ID for ownership of copies

    # 1. Create the new folder entry
    new_folder = Folder(
        name=f"{folder.name} (copy)" if parent_id == folder.parent_id else folder.name,
        created_by=current_user_id,
        parent_id=parent_id
    )
    db.session.add(new_folder)
    db.session.flush() # Flush to get new_folder.id for relationships

    # 2. Clone Documents (Database + Physical File)
    for doc in folder.documents:
        if doc.is_deleted: continue # Skip deleted docs

        try:
            # A. Decrypt original file to memory
            file_bytes = decrypt_file(doc.filepath)
            
            # B. Create a new FileStorage object
            file_obj = FileStorage(
                stream=BytesIO(file_bytes),
                filename=doc.filename,
                content_type="application/octet-stream" 
            )

            # C. Save as a NEW encrypted file (get new path)
            stored_path, stored_name = save_encrypted_file(file_obj)

            # D. Create DB Entry
            new_doc = Document(
                title=doc.title,
                filename=doc.filename,
                file_type=doc.file_type,
                tags=doc.tags,
                uploaded_by=current_user_id, # The copier becomes the owner of the copy
                folder_id=new_folder.id,
                is_active=doc.is_active,
                filepath=stored_path,
                stored_name=stored_name,
                version=1
            )
            db.session.add(new_doc)
        except Exception as e:
            print(f"Error cloning document {doc.id}: {e}")
            # Continue cloning other files even if one fails

    # 3. Recursively Clone Children Folders
    for child in folder.children:
        if not child.deleted_at:
            _clone_folder(child, new_folder.id)

    return new_folder


def _hard_delete_folder(folder: Folder):
    """Recursively permanently deletes folders and documents."""
    # Delete docs in this folder
    for doc in folder.documents:
        db.session.delete(doc) # Listener should handle file cleanup if configured

    # Recurse for children
    for child in folder.children:
        _hard_delete_folder(child)

    # Delete the folder itself
    db.session.delete(folder)


def _soft_delete_folder(folder: Folder):
    """Recursively soft deletes folders and documents (Recycle Bin)."""
    folder.is_deleted = True
    folder.deleted_at = datetime.utcnow()

    for doc in folder.documents:
        doc.is_deleted = True
        doc.deleted_at = datetime.utcnow()

    for child in folder.children:
        _soft_delete_folder(child)


# =========================
# CREATE FOLDER
# =========================
@folder_bp.route("/create", methods=["POST"])
@login_required
def create_folder():
    name = request.form.get("name", "").strip()
    parent_id = request.form.get("parent_id", type=int)

    if not name:
        flash("Folder name is required", "danger")
        return redirect(request.referrer or url_for("document.list_documents"))

    parent = Folder.query.get(parent_id) if parent_id else None

    # FIX: Ownership check with int()
    if parent and not _owns_folder(parent):
        flash("Permission denied", "danger")
        return redirect(request.referrer or url_for("document.list_documents"))

    folder = Folder(
        name=name,
        created_by=int(current_user.id), # FIX: Use int ID
        parent_id=parent.id if parent else None
    )

    db.session.add(folder)
    db.session.commit()
    
    log_activity("folder_create", details=f"Created folder '{name}'")

    return redirect(request.referrer or url_for("document.list_documents"))


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

    # Check for duplicates in the same directory
    exists = Folder.query.filter_by(
        name=new_name,
        parent_id=folder.parent_id,
        created_by=int(current_user.id) # FIX: Use int ID
    ).filter(Folder.id != folder.id).first()

    if exists:
        return jsonify(success=False, error="A folder with this name already exists here")

    old_name = folder.name
    folder.name = new_name
    db.session.commit()

    log_activity(
        action="folder_rename",
        document_id=None,
        details=f"Renamed folder from '{old_name}' to '{new_name}'"
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

    # Cannot move into itself
    if target_parent_id == folder.id:
        return jsonify(success=False, error="Invalid target"), 400

    target = Folder.query.get(target_parent_id) if target_parent_id else None

    # Check target ownership
    if target and not _owns_folder(target):
        return jsonify(success=False, error="Permission denied for target folder"), 403

    # CRITICAL: Prevent circular moves (Parent -> Child)
    if target and _is_descendant(folder, target):
        return jsonify(
            success=False,
            error="Cannot move a folder into its own subfolder"
        ), 400

    folder.parent_id = target_parent_id
    db.session.commit()

    log_activity(
        action="folder_move",
        document_id=None,
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
        return jsonify(success=False, error="Permission denied for target folder"), 403

    try:
        _clone_folder(folder, target_parent_id)
        db.session.commit()

        log_activity(
            action="folder_copy",
            document_id=None,
            details=f"Copied folder '{folder.name}'"
        )
        return jsonify(success=True)
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, error=str(e)), 500


# =========================
# FOLDER CONTENTS (API for frontend JS)
# =========================
@folder_bp.route("/<int:folder_id>/contents")
@login_required
def folder_contents(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    # FIX: Ensure int comparison
    if not (current_user.is_admin or folder.created_by == int(current_user.id)):
        return jsonify(success=False, error="Permission denied"), 403

    documents = [
        {
            "id": d.id,
            "title": d.title,
            "type": d.file_type,
            "created_at": d.created_at.strftime("%Y-%m-%d")
        }
        for d in folder.documents if not d.is_deleted
    ]
    
    subfolders = [
        {
            "id": f.id,
            "name": f.name,
            "created_at": f.created_at.strftime("%Y-%m-%d")
        }
        for f in folder.children if not f.deleted_at
    ]

    return jsonify(
        folder={"id": folder.id, "name": folder.name},
        documents=documents,
        subfolders=subfolders
    )


# =========================
# MOVE TO RECYCLE BIN
# =========================
@folder_bp.route("/<int:folder_id>/bin", methods=["POST"])
@login_required
def move_folder_to_bin(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    if not _owns_folder(folder):
        return jsonify(success=False, error="Permission denied. You do not own this folder."), 403

    _soft_delete_folder(folder)
    db.session.commit()

    log_activity(
        action="folder_bin",
        document_id=None,
        details=f"Moved folder '{folder.name}' to recycle bin"
    )

    return jsonify(success=True)


# =========================
# PERMANENT DELETE
# =========================
@folder_bp.route("/<int:folder_id>/delete", methods=["POST"])
@login_required
def delete_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    if not _owns_folder(folder):
        return jsonify(success=False, error="Permission denied. You do not own this folder."), 403

    folder_name = folder.name

    _hard_delete_folder(folder)
    db.session.commit()

    log_activity(
        action="folder_permanent_delete",
        document_id=None,
        details=f"Permanently deleted folder '{folder_name}'"
    )

    return jsonify(success=True)


# =========================
# BULK DELETE SUPPORT
# =========================
@folder_bp.route("/bulk/bin", methods=["POST"])
@login_required
def bulk_folder_move_to_bin():
    data = request.get_json(silent=True) or {}
    ids = data.get("ids", [])

    if not isinstance(ids, list):
        return jsonify(success=False, error="Invalid payload"), 400

    folders = Folder.query.filter(Folder.id.in_(ids)).all()

    count = 0
    for folder in folders:
        # _owns_folder already includes the int() fix
        if _owns_folder(folder):
            _soft_delete_folder(folder)
            count += 1

    db.session.commit()
    return jsonify(success=True, count=count)


@folder_bp.route("/bulk/delete", methods=["POST"])
@login_required
def bulk_folder_delete():
    data = request.get_json(silent=True) or {}
    ids = data.get("ids", [])

    if not isinstance(ids, list):
        return jsonify(success=False, error="Invalid payload"), 400

    folders = Folder.query.filter(Folder.id.in_(ids)).all()

    count = 0
    for folder in folders:
        # _owns_folder already includes the int() fix
        if _owns_folder(folder):
            _hard_delete_folder(folder)
            count += 1

    db.session.commit()
    return jsonify(success=True, count=count)