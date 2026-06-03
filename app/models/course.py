"""
app/models/course.py
────────────────────
Course and Category models.
"""
from datetime import datetime, timezone

from app import db

# ── Association table for course tags ─────────────────────────────────────────
course_tags = db.Table(
    "course_tags",
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(64), default="bi-folder")

    courses = db.relationship("Course", back_populates="category", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Category {self.name}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)


class Course(db.Model):
    __tablename__ = "courses"

    LEVEL_BEGINNER = "Beginner"
    LEVEL_INTERMEDIATE = "Intermediate"
    LEVEL_ADVANCED = "Advanced"
    LEVELS = [LEVEL_BEGINNER, LEVEL_INTERMEDIATE, LEVEL_ADVANCED]

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(300), nullable=True)
    thumbnail_url = db.Column(db.String(512), nullable=True)
    level = db.Column(db.String(20), default="Beginner")
    duration_hours = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    price = db.Column(db.Numeric(8, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Foreign keys
    instructor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)

    # Relationships
    instructor = db.relationship("User", back_populates="courses_taught", foreign_keys=[instructor_id])
    category = db.relationship("Category", back_populates="courses")
    enrollments = db.relationship("Enrollment", back_populates="course", lazy="dynamic")
    materials = db.relationship(
        "CourseMaterial", back_populates="course",
        lazy="dynamic", cascade="all, delete-orphan",
        order_by="CourseMaterial.order_index"
    )
    tags = db.relationship("Tag", secondary=course_tags, lazy="subquery",
                           backref=db.backref("courses", lazy=True))

    # ── Computed helpers ──────────────────────────────────────────────────────
    @property
    def student_count(self) -> int:
        return self.enrollments.count()

    @property
    def material_count(self) -> int:
        return self.materials.count()

    @property
    def is_free(self) -> bool:
        return float(self.price or 0) == 0.0

    def is_enrolled(self, user) -> bool:
        """Check whether *user* is enrolled in this course."""
        from app.models.enrollment import Enrollment
        return (
            Enrollment.query
            .filter_by(student_id=user.id, course_id=self.id)
            .first() is not None
        )

    def __repr__(self) -> str:
        return f"<Course {self.title!r}>"
