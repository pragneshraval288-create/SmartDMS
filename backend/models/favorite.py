from datetime import datetime
from ..extensions import db


# =========================
# DOCUMENT FAVORITE
# =========================
class DocumentFavorite(db.Model):
    __tablename__ = "document_favorites"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # relationships
    user = db.relationship(
        "User",
        backref=db.backref(
            "favorite_documents",
            cascade="all, delete-orphan",
            lazy="select"
        )
    )

    document = db.relationship(
        "Document",
        backref=db.backref(
            "favorited_by",
            cascade="all, delete-orphan",
            lazy="select"
        )
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "document_id",
            name="uq_user_document_favorite"
        ),
    )

    def __repr__(self):
        return (
            f"<DocumentFavorite user_id={self.user_id} "
            f"document_id={self.document_id}>"
        )


# =========================
# FOLDER FAVORITE
# =========================
class FolderFavorite(db.Model):
    __tablename__ = "folder_favorites"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    folder_id = db.Column(
        db.Integer,
        db.ForeignKey("folders.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # relationships
    user = db.relationship(
        "User",
        backref=db.backref(
            "favorite_folders",
            cascade="all, delete-orphan",
            lazy="select"
        )
    )

    folder = db.relationship(
        "Folder",
        backref=db.backref(
            "favorited_by",
            cascade="all, delete-orphan",
            lazy="select"
        )
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "folder_id",
            name="uq_user_folder_favorite"
        ),
    )

    def __repr__(self):
        return (
            f"<FolderFavorite user_id={self.user_id} "
            f"folder_id={self.folder_id}>"
        )
