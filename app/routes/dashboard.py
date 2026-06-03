"""
app/routes/dashboard.py
────────────────────────
Dashboard for logged-in users (students & instructors).
"""
from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.services.course_service import (
    get_instructor_courses,
    get_student_enrollments,
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    if current_user.is_instructor:
        return _instructor_dashboard()
    return _student_dashboard()


def _student_dashboard():
    enrollments = get_student_enrollments(current_user.id)
    return render_template(
        "dashboard/student.html",
        enrollments=enrollments,
    )


def _instructor_dashboard():
    courses = get_instructor_courses(current_user.id)
    return render_template(
        "dashboard/instructor.html",
        courses=courses,
    )
