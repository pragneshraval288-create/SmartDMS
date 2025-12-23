from datetime import datetime
from ..extensions import db


class Folder(db.Model):
    __tablename__ = "folders"

    # ======================
    # COLUMNS
    # ======================

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("folders.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    # 🔥 RECYCLE BIN FIELDS
    is_deleted = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        index=True
    )

    deleted_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # ======================
    # RELATIONSHIPS
    # ======================

    # 🔁 parent → children (self-referential)
    parent = db.relationship(
        "Folder",
        remote_side=[id],
        backref=db.backref(
            "children",
            cascade="all, delete",
            passive_deletes=True,
            lazy="select"
        )
    )

    # 📄 folder → documents
    # ❗ NO delete-orphan (folder delete = docs move to root)
    documents = db.relationship(
        "Document",
        back_populates="folder",
        lazy="select"
    )

    # ======================
    # HELPERS
    # ======================

    def is_root(self) -> bool:
        return self.parent_id is None

    def all_descendants(self):
        """
        Return all subfolders recursively.
        Used for move / copy validation.
        """
        result = []
        for child in self.children:
            result.append(child)
            result.extend(child.all_descendants())
        return result

    def __repr__(self):
        return (
            f"<Folder id={self.id} "
            f"name='{self.name}' "
            f"favorite={self.is_favorite} "
            f"deleted={self.is_deleted} "
            f"parent_id={self.parent_id}>"
        )
