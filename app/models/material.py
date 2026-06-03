"""
app/models/material.py
──────────────────────
Course material/content uploaded by instructors.
"""
from datetime import datetime, timezone

from app import db


class CourseMaterial(db.Model):
    __tablename__ = "course_materials"

    TYPE_DOCUMENT = "document"
    TYPE_VIDEO = "video"
    TYPE_IMAGE = "image"
    TYPE_ARCHIVE = "archive"
    TYPE_OTHER = "other"

    EXTENSION_TYPE_MAP = {
        "pdf": TYPE_DOCUMENT,
        "docx": TYPE_DOCUMENT,
        "pptx": TYPE_DOCUMENT,
        "mp4": TYPE_VIDEO,
        "webm": TYPE_VIDEO,
        "png": TYPE_IMAGE,
        "jpg": TYPE_IMAGE,
        "jpeg": TYPE_IMAGE,
        "gif": TYPE_IMAGE,
        "zip": TYPE_ARCHIVE,
    }

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(300), nullable=False)      # stored filename (safe)
    original_filename = db.Column(db.String(300), nullable=False)
    storage_key = db.Column(db.String(512), nullable=False)   # S3 key or local path
    file_type = db.Column(db.String(20), default=TYPE_OTHER)
    file_size = db.Column(db.Integer, default=0)              # bytes
    order_index = db.Column(db.Integer, default=0)
    is_preview = db.Column(db.Boolean, default=False)         # visible without enrollment
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    course = db.relationship("Course", back_populates="materials")
    uploader = db.relationship("User")

    @classmethod
    def guess_type(cls, extension: str) -> str:
        return cls.EXTENSION_TYPE_MAP.get(extension.lower(), cls.TYPE_OTHER)

    @property
    def size_display(self) -> str:
        size = self.file_size or 0
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    @property
    def icon_class(self) -> str:
        icons = {
            self.TYPE_DOCUMENT: "bi-file-earmark-text",
            self.TYPE_VIDEO: "bi-play-circle",
            self.TYPE_IMAGE: "bi-image",
            self.TYPE_ARCHIVE: "bi-file-zip",
        }
        return icons.get(self.file_type, "bi-file-earmark")

    def __repr__(self) -> str:
        return f"<CourseMaterial {self.title!r} (course={self.course_id})>"
