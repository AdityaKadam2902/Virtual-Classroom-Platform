"""
app/models/user.py
──────────────────
User model with role support (student, instructor, admin).
Uses Flask-Login's UserMixin for session management.
"""
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager

# ── Role constants ────────────────────────────────────────────────────────────
ROLE_STUDENT = "student"
ROLE_INSTRUCTOR = "instructor"
ROLE_ADMIN = "admin"
VALID_ROLES = {ROLE_STUDENT, ROLE_INSTRUCTOR, ROLE_ADMIN}


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=ROLE_STUDENT)
    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(512), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    enrollments = db.relationship(
        "Enrollment", back_populates="student", lazy="dynamic",
        foreign_keys="Enrollment.student_id"
    )
    courses_taught = db.relationship(
        "Course", back_populates="instructor", lazy="dynamic",
        foreign_keys="Course.instructor_id"
    )

    # ── Password ──────────────────────────────────────────────────────────────
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # ── Role helpers ──────────────────────────────────────────────────────────
    @property
    def is_admin(self) -> bool:
        return self.role == ROLE_ADMIN

    @property
    def is_instructor(self) -> bool:
        return self.role in (ROLE_INSTRUCTOR, ROLE_ADMIN)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def record_login(self) -> None:
        self.last_login = datetime.now(timezone.utc)
        db.session.commit()

    def __repr__(self) -> str:
        return f"<User {self.email} [{self.role}]>"


# ── Flask-Login user loader ───────────────────────────────────────────────────
@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))
