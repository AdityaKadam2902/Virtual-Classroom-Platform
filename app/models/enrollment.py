"""
app/models/enrollment.py
────────────────────────
Student ↔ Course enrollment with progress tracking.
"""
from datetime import datetime, timezone

from app import db


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    __table_args__ = (
        db.UniqueConstraint("student_id", "course_id", name="uq_enrollment"),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    progress = db.Column(db.Integer, default=0)  # 0-100 percentage
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    student = db.relationship("User", back_populates="enrollments", foreign_keys=[student_id])
    course = db.relationship("Course", back_populates="enrollments")

    def mark_complete(self) -> None:
        self.completed = True
        self.progress = 100
        self.completed_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<Enrollment user={self.student_id} course={self.course_id}>"
