from datetime import datetime
from ..extensions import db


class DocumentShare(db.Model):
    __tablename__ = "document_shares"

    id = db.Column(db.Integer, primary_key=True)

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    shared_with_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    can_edit = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    document = db.relationship(
        "Document",
        back_populates="shares",
        lazy="select"
    )

    shared_with = db.relationship(
        "User",
        lazy="select"
    )

    def __repr__(self):
        return (
            f"<DocumentShare id={self.id} "
            f"doc_id={self.document_id} "
            f"shared_with={self.shared_with_id}>"
        )
