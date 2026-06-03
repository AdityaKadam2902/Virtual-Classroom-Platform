"""
app/services/course_service.py
───────────────────────────────
Business logic for course CRUD, enrollment, and material management.
"""
import re
from typing import Optional

from flask import current_app
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.course import Category, Course
from app.models.enrollment import Enrollment
from app.models.material import CourseMaterial
from app.services.storage import get_storage


class AlreadyEnrolledError(Exception):
    pass


def _slugify(text: str) -> str:
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug[:220]


def _unique_slug(title: str) -> str:
    base = _slugify(title)
    slug = base
    counter = 1
    while Course.query.filter_by(slug=slug).first():
        slug = f"{base}-{counter}"
        counter += 1
    return slug


# ── Course CRUD ───────────────────────────────────────────────────────────────

def create_course(
    title: str,
    description: str,
    short_description: str,
    instructor_id: int,
    level: str = Course.LEVEL_BEGINNER,
    duration_hours: int = 0,
    price: float = 0.0,
    category_id: Optional[int] = None,
    thumbnail_url: Optional[str] = None,
    is_published: bool = False,
) -> Course:
    course = Course(
        title=title.strip(),
        slug=_unique_slug(title),
        description=description.strip(),
        short_description=short_description.strip(),
        instructor_id=instructor_id,
        level=level,
        duration_hours=duration_hours,
        price=price,
        category_id=category_id if category_id else None,
        thumbnail_url=thumbnail_url,
        is_published=is_published,
    )
    db.session.add(course)
    db.session.commit()
    current_app.logger.info("Course created: %s (id=%s)", course.title, course.id)
    return course


def update_course(course: Course, **kwargs) -> Course:
    allowed = {
        "title", "description", "short_description", "level",
        "duration_hours", "price", "category_id", "thumbnail_url", "is_published",
    }
    for key, value in kwargs.items():
        if key in allowed:
            setattr(course, key, value)
    db.session.commit()
    return course


def delete_course(course: Course) -> None:
    # Delete associated materials from storage first
    for material in course.materials:
        try:
            get_storage().delete(material.storage_key)
        except Exception as exc:
            current_app.logger.warning("Could not delete material %s: %s", material.storage_key, exc)
    db.session.delete(course)
    db.session.commit()


def get_course_by_slug(slug: str) -> Optional[Course]:
    return Course.query.filter_by(slug=slug).first()


def get_course_by_id(course_id: int) -> Optional[Course]:
    return db.session.get(Course, course_id)


def list_published_courses(
    q: str = "",
    level: str = "",
    category_id: int = 0,
    page: int = 1,
    per_page: int = 12,
):
    query = Course.query.filter_by(is_published=True)
    if q:
        term = f"%{q}%"
        query = query.filter(
            or_(Course.title.ilike(term), Course.short_description.ilike(term))
        )
    if level:
        query = query.filter_by(level=level)
    if category_id:
        query = query.filter_by(category_id=category_id)
    return query.order_by(Course.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )


# ── Enrollment ────────────────────────────────────────────────────────────────

def enroll_student(student_id: int, course_id: int) -> Enrollment:
    existing = Enrollment.query.filter_by(
        student_id=student_id, course_id=course_id
    ).first()
    if existing:
        raise AlreadyEnrolledError("Already enrolled in this course.")
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return enrollment


def get_student_enrollments(student_id: int):
    return (
        Enrollment.query
        .filter_by(student_id=student_id)
        .join(Enrollment.course)
        .filter(Course.is_published == True)  # noqa: E712
        .order_by(Enrollment.enrolled_at.desc())
        .all()
    )


def get_instructor_courses(instructor_id: int, page: int = 1, per_page: int = 12):
    return (
        Course.query
        .filter_by(instructor_id=instructor_id)
        .order_by(Course.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )


# ── Materials ─────────────────────────────────────────────────────────────────

def upload_material(
    course: Course,
    uploader_id: int,
    file,
    title: str,
    description: str = "",
    is_preview: bool = False,
) -> CourseMaterial:
    storage = get_storage()
    result = storage.upload(
        file_obj=file,
        original_filename=file.filename,
        folder=f"courses/{course.id}",
    )
    ext = result["filename"].rsplit(".", 1)[-1] if "." in result["filename"] else ""
    material = CourseMaterial(
        course_id=course.id,
        uploader_id=uploader_id,
        title=title.strip(),
        description=description.strip(),
        filename=result["filename"],
        original_filename=file.filename,
        storage_key=result["storage_key"],
        file_type=CourseMaterial.guess_type(ext),
        file_size=result["file_size"],
        is_preview=is_preview,
        order_index=course.materials.count(),
    )
    db.session.add(material)
    db.session.commit()
    return material


def delete_material(material: CourseMaterial) -> None:
    try:
        get_storage().delete(material.storage_key)
    except Exception as exc:
        current_app.logger.warning("Storage delete failed for %s: %s", material.storage_key, exc)
    db.session.delete(material)
    db.session.commit()


# ── Categories ────────────────────────────────────────────────────────────────

def all_categories():
    return Category.query.order_by(Category.name).all()


def get_or_create_category(name: str) -> Category:
    slug = _slugify(name)
    cat = Category.query.filter_by(slug=slug).first()
    if not cat:
        cat = Category(name=name.strip(), slug=slug)
        db.session.add(cat)
        db.session.commit()
    return cat
