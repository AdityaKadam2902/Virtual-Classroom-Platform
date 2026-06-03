"""
tests/conftest.py
─────────────────
Simple, reliable test fixtures.
Each test gets a fresh in-memory DB via function-scoped app + client.
"""
import pytest

from app import create_app, db as _db
from app.config import TestingConfig
from app.models.user import User, ROLE_STUDENT, ROLE_INSTRUCTOR, ROLE_ADMIN
from app.models.course import Category, Course


@pytest.fixture()
def app():
    """Fresh app + empty in-memory DB for every test."""
    application = create_app(TestingConfig)
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


# ── Model factories ───────────────────────────────────────────

def _make_user(email, role, first="Test", last="User", password="Test1234"):
    u = User(first_name=first, last_name=last, email=email, role=role)
    u.set_password(password)
    _db.session.add(u)
    _db.session.flush()
    return u


@pytest.fixture()
def student(app):
    with app.app_context():
        return _make_user("student@test.com", ROLE_STUDENT, "Sam", "Student")


@pytest.fixture()
def instructor(app):
    with app.app_context():
        return _make_user("instructor@test.com", ROLE_INSTRUCTOR, "Iris", "Instructor")


@pytest.fixture()
def category(app):
    with app.app_context():
        cat = Category(name="Testing", slug="testing", icon="bi-bug")
        _db.session.add(cat)
        _db.session.flush()
        return cat


@pytest.fixture()
def published_course(app, instructor, category):
    with app.app_context():
        c = Course(
            title="Test Course",
            slug="test-course",
            description="A test course description that is long enough.",
            short_description="Short test description.",
            instructor_id=instructor.id,
            category_id=category.id,
            level="Beginner",
            is_published=True,
        )
        _db.session.add(c)
        _db.session.flush()
        return c
