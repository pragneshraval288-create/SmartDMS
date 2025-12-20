from datetime import datetime
from ..extensions import db


class DocumentComment(db.Model):
    __tablename__ = "document_comments"

    id = db.Column(db.Integer, primary_key=True)

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    document = db.relationship(
        "Document",
        back_populates="comments",
        lazy="select"
    )

    author = db.relationship(
        "User",
        back_populates="comments",
        lazy="select"
    )

    def __repr__(self):
        return (
            f"<DocumentComment id={self.id} "
            f"doc_id={self.document_id} "
            f"user_id={self.user_id}>"
        )
