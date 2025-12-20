import os
from datetime import datetime
from werkzeug.datastructures import FileStorage

from ..extensions import db
from ..models import Document, DocumentVersion, User
from .storage_service import save_encrypted_file
from .activity_service import log_activity
from .notification_service import notify_user


# ======================================================
# CREATE DOCUMENT (FOLDER-AWARE)
# ======================================================
def create_document(
    user: User,
    title: str,
    tags: str | None,
    file_storage: FileStorage,
    folder_id: int | None = None,
) -> Document:

    # ------------------------------
    # FILE EXTENSION
    # ------------------------------
    _, ext = os.path.splitext(file_storage.filename)
    ext = ext.replace(".", "").lower()

    stored_path, stored_name = save_encrypted_file(file_storage)

    # ------------------------------
    # DOCUMENT (VERSION = 1)
    # ------------------------------
    doc = Document(
        title=title,
        tags=tags,
        filename=file_storage.filename,
        stored_name=stored_name,
        filepath=stored_path,
        file_type=ext,
        uploaded_by=user.id,
        folder_id=folder_id,
        version=1,
        is_active=True,
        created_at=datetime.utcnow(),
    )

    db.session.add(doc)
    db.session.flush()  # 🔥 get doc.id safely

    # ------------------------------
    # VERSION ROW (v1)
    # ------------------------------
    version_row = DocumentVersion(
        document_id=doc.id,
        version=1,
        stored_name=stored_name,
        filepath=stored_path,
    )

    db.session.add(version_row)
    db.session.commit()

    # ------------------------------
    # ACTIVITY + NOTIFICATION
    # ------------------------------
    log_activity(
        action="upload",
        document_id=doc.id,
        details="Document uploaded"
    )

    notify_user(
        user,
        f"Document '{doc.title}' uploaded successfully."
    )

    return doc


# ======================================================
# UPDATE DOCUMENT FILE (NEW VERSION)
# ======================================================
def update_document_file(
    doc: Document,
    file_storage: FileStorage
) -> Document:

    new_version = (doc.version or 1) + 1

    # ------------------------------
    # FILE EXTENSION
    # ------------------------------
    _, ext = os.path.splitext(file_storage.filename)
    ext = ext.replace(".", "").lower()

    stored_path, stored_name = save_encrypted_file(
        file_storage,
        version_suffix=f"_v{new_version}"
    )

    # ------------------------------
    # UPDATE DOCUMENT
    # ------------------------------
    doc.version = new_version
    doc.file_type = ext
    doc.filename = file_storage.filename
    doc.stored_name = stored_name
    doc.filepath = stored_path
    doc.updated_at = datetime.utcnow()

    # ------------------------------
    # VERSION ROW
    # ------------------------------
    version_row = DocumentVersion(
        document_id=doc.id,
        version=new_version,
        stored_name=stored_name,
        filepath=stored_path,
    )

    db.session.add(version_row)
    db.session.commit()

    # ------------------------------
    # ACTIVITY + NOTIFICATION
    # ------------------------------
    log_activity(
        "update",
        document_id=doc.id,
        details=f"Updated file to version {new_version}"
    )

    notify_user(
        doc.uploader,
        f"Your document '{doc.title}' has a new version ({new_version})."
    )

    return doc


# ======================================================
# ARCHIVE / RESTORE / DOWNLOAD
# ======================================================
def soft_archive(doc: Document):
    doc.is_active = False
    db.session.commit()

    log_activity(
        "archive",
        document_id=doc.id,
        details="Document archived"
    )


def restore(doc: Document):
    doc.is_active = True
    db.session.commit()

    log_activity(
        "restore",
        document_id=doc.id,
        details="Document restored"
    )


def increment_download(doc: Document):
    doc.download_count = (doc.download_count or 0) + 1
    db.session.commit()

    log_activity(
        "download",
        document_id=doc.id,
        details="Document downloaded"
    )
