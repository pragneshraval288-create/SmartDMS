# backend/routes/favorite.py

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user

from ..extensions import db
from ..models import (
    Document,
    Folder,
    DocumentFavorite,
    FolderFavorite
)

favorites_bp = Blueprint(
    "favorites",
    __name__,
    url_prefix="/favorites"
)

# ==================================================
# FAVORITES PAGE
# ==================================================
@favorites_bp.route("/")
@login_required
def index():
    """
    Show all favorite documents and folders
    for the logged-in user.
    """

    # ⭐ Favorite Documents
    favorite_documents = (
        Document.query
        .join(
            DocumentFavorite,
            Document.id == DocumentFavorite.document_id
        )
        .filter(
            DocumentFavorite.user_id == current_user.id,
            Document.is_deleted.is_(False)
        )
        .order_by(DocumentFavorite.created_at.desc())
        .all()
    )

    # ⭐ Favorite Folders
    favorite_folders = (
        Folder.query
        .join(
            FolderFavorite,
            Folder.id == FolderFavorite.folder_id
        )
        .filter(
            FolderFavorite.user_id == current_user.id,
            Folder.is_deleted.is_(False)
        )
        .order_by(FolderFavorite.created_at.desc())
        .all()
    )

    return render_template(
        "favorites/index.html",
        documents=favorite_documents,
        folders=favorite_folders
    )


# ==================================================
# ⭐ TOGGLE DOCUMENT FAVORITE
# ==================================================
@favorites_bp.route("/document/<int:document_id>/toggle", methods=["POST"])
@login_required
def toggle_document_favorite(document_id):
    doc = Document.query.get_or_404(document_id)

    fav = DocumentFavorite.query.filter_by(
        user_id=current_user.id,
        document_id=document_id
    ).first()

    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify(success=True, favorited=False)

    new_fav = DocumentFavorite(
        user_id=current_user.id,
        document_id=document_id
    )
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(success=True, favorited=True)


# ==================================================
# ⭐ TOGGLE FOLDER FAVORITE
# ==================================================
@favorites_bp.route("/folder/<int:folder_id>/toggle", methods=["POST"])
@login_required
def toggle_folder_favorite(folder_id):
    folder = Folder.query.get_or_404(folder_id)

    fav = FolderFavorite.query.filter_by(
        user_id=current_user.id,
        folder_id=folder_id
    ).first()

    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify(success=True, favorited=False)

    new_fav = FolderFavorite(
        user_id=current_user.id,
        folder_id=folder_id
    )
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(success=True, favorited=True)
