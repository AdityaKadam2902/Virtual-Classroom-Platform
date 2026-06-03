"""
tests/test_courses.py
─────────────────────
Tests for course listing, detail, enrollment, and service layer.
"""
import pytest

from app import db as _db, db
from app.models.enrollment import Enrollment
from app.services.course_service import (
    AlreadyEnrolledError,
    create_course,
    enroll_student,
    get_course_by_slug,
    list_published_courses,
)


class TestCoursePages:
    def test_course_index_loads(self, client):
        r = client.get("/courses/")
        assert r.status_code == 200
        assert b"Courses" in r.data

    def test_course_index_search(self, client, published_course):
        r = client.get("/courses/?q=Test")
        assert r.status_code == 200

    def test_course_detail_published(self, client, app):
        # Create and commit a course so the test-client request can find it
        with app.app_context():
            from app.models.user import User, ROLE_INSTRUCTOR
            from app.models.course import Course
            u = User(first_name="T", last_name="T", email="tc@test.com", role=ROLE_INSTRUCTOR)
            u.set_password("Test1234")
            _db.session.add(u)
            _db.session.flush()
            c = Course(
                title="Visible Course",
                slug="visible-course",
                description="A long enough description.",
                short_description="Short.",
                instructor_id=u.id,
                is_published=True,
            )
            _db.session.add(c)
            _db.session.commit()
        r = client.get("/courses/visible-course")
        assert r.status_code == 200
        assert b"Visible Course" in r.data

    def test_course_detail_404_for_unknown_slug(self, client):
        r = client.get("/courses/does-not-exist-xyz")
        assert r.status_code == 404

    def test_enroll_requires_login(self, client, published_course):
        client.get("/auth/logout")
        r = client.post(
            f"/courses/{published_course.slug}/enroll",
            follow_redirects=True,
        )
        assert b"Sign In" in r.data or b"log in" in r.data.lower()


class TestCourseService:
    def test_create_course(self, app, instructor):
        course = create_course(
            title="Service Test Course",
            description="A sufficiently long description for the test.",
            short_description="Short desc.",
            instructor_id=instructor.id,
            is_published=True,
        )
        assert course.id is not None
        assert course.slug == "service-test-course"

    def test_slug_uniqueness(self, app, instructor):
        c1 = create_course(
            title="Duplicate Title",
            description="Description one is long enough.",
            short_description="Short.",
            instructor_id=instructor.id,
        )
        c2 = create_course(
            title="Duplicate Title",
            description="Description two is long enough.",
            short_description="Short.",
            instructor_id=instructor.id,
        )
        assert c1.slug != c2.slug

    def test_get_course_by_slug(self, app, instructor):
        with app.app_context():
            c = create_course(
                title="Slug Lookup Course",
                description="Long enough description for the test here.",
                short_description="Short.",
                instructor_id=instructor.id,
                is_published=True,
            )
            _db.session.commit()
            found = get_course_by_slug(c.slug)
            assert found is not None
            assert found.title == "Slug Lookup Course"

    def test_get_course_by_slug_missing(self, app):
        assert get_course_by_slug("not-a-real-slug") is None

    def test_list_published_courses_excludes_drafts(self, app, instructor, category):
        from app.models.course import Course
        draft = Course(
            title="Draft Course",
            slug="draft-course-unique",
            description="Draft.",
            short_description="Draft short.",
            instructor_id=instructor.id,
            is_published=False,
        )
        db.session.add(draft)
        db.session.flush()
        results = list_published_courses()
        slugs = [c.slug for c in results.items]
        assert "draft-course-unique" not in slugs

    def test_list_published_courses_filter_by_level(self, app, published_course):
        results = list_published_courses(level="Beginner")
        assert all(c.level == "Beginner" for c in results.items)


class TestEnrollment:
    def test_enroll_student(self, app, student, published_course):
        enroll = enroll_student(student.id, published_course.id)
        assert enroll.id is not None
        assert enroll.student_id == student.id
        assert enroll.course_id == published_course.id

    def test_double_enroll_raises(self, app, student, published_course):
        enroll_student(student.id, published_course.id)
        with pytest.raises(AlreadyEnrolledError):
            enroll_student(student.id, published_course.id)

    def test_enrollment_initial_progress_zero(self, app, student, published_course):
        # Use a distinct student to avoid collision with other enrollment tests
        from app.models.user import User, ROLE_STUDENT
        u2 = User(first_name="Z", last_name="Z", email="z2@test.com", role=ROLE_STUDENT)
        u2.set_password("Test1234")
        db.session.add(u2)
        db.session.flush()
        enroll = enroll_student(u2.id, published_course.id)
        assert enroll.progress == 0
        assert enroll.completed is False
