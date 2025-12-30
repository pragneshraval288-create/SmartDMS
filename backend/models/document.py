from datetime import datetime
from ..extensions import db
from ..services.encryption_service import EncryptionService


# ======================
# DOCUMENT MODEL
# ======================
class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)

    # 🔐 ENCRYPTED COLUMNS (stored encrypted in DB)
    _title = db.Column("title", db.String(255), nullable=False, index=True)
    _tags = db.Column("tags", db.String(255), nullable=True)
    _category = db.Column("category", db.String(100), nullable=True, index=True)

    filename = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(20), nullable=True)

    version = db.Column(db.Integer, nullable=False, default=1)

    is_active = db.Column(db.Boolean, default=True)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending",
        index=True
    )

    # 🔥 RECYCLE BIN FIELDS
    is_deleted = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        index=True
    )

    deleted_at = db.Column(db.DateTime, nullable=True)

    uploaded_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    uploader = db.relationship(
        "User",
        back_populates="documents",
        lazy="select"
    )

    folder_id = db.Column(
        db.Integer,
        db.ForeignKey("folders.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    folder = db.relationship(
        "Folder",
        back_populates="documents",
        lazy="select"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    expiry_date = db.Column(db.Date, nullable=True)
    download_count = db.Column(db.Integer, default=0)

    # ======================
    # RELATIONSHIPS
    # ======================

    versions = db.relationship(
        "DocumentVersion",
        back_populates="document",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="select",
        order_by="DocumentVersion.version.desc()"
    )

    comments = db.relationship(
        "DocumentComment",
        back_populates="document",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="select"
    )

    shares = db.relationship(
        "DocumentShare",
        back_populates="document",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="select"
    )

    # ======================
    # 🔐 TRANSPARENT ENCRYPTION
    # ======================

    @property
    def title(self):
        return EncryptionService.decrypt_text(self._title)

    @title.setter
    def title(self, value):
        self._title = EncryptionService.encrypt_text(value)

    @property
    def tags(self):
        return EncryptionService.decrypt_text(self._tags)

    @tags.setter
    def tags(self, value):
        self._tags = EncryptionService.encrypt_text(value)

    @property
    def category(self):
        return EncryptionService.decrypt_text(self._category)

    @category.setter
    def category(self, value):
        self._category = EncryptionService.encrypt_text(value)

    # ======================
    # SAFE REPR (🔥 FIX)
    # ======================
    def __repr__(self):
        return (
            f"<Document id={self.id} "
            f"deleted={self.is_deleted}>"
        )


# ======================
# DOCUMENT VERSION
# ======================
class DocumentVersion(db.Model):
    __tablename__ = "document_versions"

    id = db.Column(db.Integer, primary_key=True)

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    version = db.Column(db.Integer, nullable=False)

    stored_name = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    document = db.relationship(
        "Document",
        back_populates="versions",
        lazy="select"
    )

    def __repr__(self):
        return f"<DocumentVersion doc_id={self.document_id} v={self.version}>"
