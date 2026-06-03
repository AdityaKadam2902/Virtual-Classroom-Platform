"""
app/routes/courses.py
─────────────────────
Course browsing, detail, enrollment, and material download.
"""
from flask import (
    Blueprint, abort, flash, redirect, render_template,
    request, send_file, url_for,
)
from flask_login import current_user, login_required

from app.forms.course import CourseForm, CourseSearchForm, MaterialUploadForm
from app.models.course import Course
from app.services.course_service import (
    AlreadyEnrolledError,
    all_categories,
    create_course,
    delete_material,
    enroll_student,
    get_course_by_slug,
    get_instructor_courses,
    list_published_courses,
    update_course,
    upload_material,
)
from app.utils.decorators import instructor_required

courses_bp = Blueprint("courses", __name__)


# ── Public: course listing ────────────────────────────────────────────────────

@courses_bp.route("/")
def index():
    categories = all_categories()
    form = CourseSearchForm(request.args)
    # Populate category choices dynamically
    form.category.choices = [(0, "All Categories")] + [
        (c.id, c.name) for c in categories
    ]

    courses = list_published_courses(
        q=form.q.data or "",
        level=form.level.data or "",
        category_id=int(form.category.data or 0),
        page=request.args.get("page", 1, type=int),
    )
    return render_template(
        "courses/index.html",
        courses=courses,
        form=form,
        categories=categories,
    )


# ── Public: course detail ─────────────────────────────────────────────────────

@courses_bp.route("/<slug>")
def detail(slug: str):
    course = get_course_by_slug(slug)
    if not course or not course.is_published:
        abort(404)

    enrolled = False
    if current_user.is_authenticated:
        enrolled = course.is_enrolled(current_user)

    # Show preview materials + all if enrolled/instructor/admin
    if enrolled or (current_user.is_authenticated and current_user.is_instructor):
        materials = course.materials.all()
    else:
        materials = course.materials.filter_by(is_preview=True).all()

    return render_template(
        "courses/detail.html",
        course=course,
        enrolled=enrolled,
        materials=materials,
    )


# ── Enrollment ────────────────────────────────────────────────────────────────

@courses_bp.route("/<slug>/enroll", methods=["POST"])
@login_required
def enroll(slug: str):
    course = get_course_by_slug(slug)
    if not course or not course.is_published:
        abort(404)
    try:
        enroll_student(current_user.id, course.id)
        flash(f"You are now enrolled in «{course.title}»!", "success")
    except AlreadyEnrolledError:
        flash("You are already enrolled in this course.", "info")
    return redirect(url_for("courses.detail", slug=slug))


# ── Instructor: create course ─────────────────────────────────────────────────

@courses_bp.route("/new", methods=["GET", "POST"])
@login_required
@instructor_required
def create():
    form = CourseForm()
    categories = all_categories()
    form.category_id.choices = [(0, "— None —")] + [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        course = create_course(
            title=form.title.data,
            description=form.description.data,
            short_description=form.short_description.data,
            instructor_id=current_user.id,
            level=form.level.data,
            duration_hours=form.duration_hours.data or 0,
            price=float(form.price.data or 0),
            category_id=form.category_id.data or None,
            thumbnail_url=form.thumbnail_url.data or None,
            is_published=form.is_published.data,
        )
        flash(f"Course «{course.title}» created!", "success")
        return redirect(url_for("courses.detail", slug=course.slug))

    return render_template("courses/form.html", form=form, title="Create Course")


# ── Instructor: edit course ───────────────────────────────────────────────────

@courses_bp.route("/<slug>/edit", methods=["GET", "POST"])
@login_required
@instructor_required
def edit(slug: str):
    course = get_course_by_slug(slug)
    if not course:
        abort(404)
    if not current_user.is_admin and course.instructor_id != current_user.id:
        abort(403)

    categories = all_categories()
    form = CourseForm(obj=course)
    form.category_id.choices = [(0, "— None —")] + [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        update_course(
            course,
            title=form.title.data,
            description=form.description.data,
            short_description=form.short_description.data,
            level=form.level.data,
            duration_hours=form.duration_hours.data or 0,
            price=float(form.price.data or 0),
            category_id=form.category_id.data or None,
            thumbnail_url=form.thumbnail_url.data or None,
            is_published=form.is_published.data,
        )
        flash("Course updated.", "success")
        return redirect(url_for("courses.detail", slug=course.slug))

    return render_template("courses/form.html", form=form, course=course, title="Edit Course")


# ── Material upload ───────────────────────────────────────────────────────────

@courses_bp.route("/<slug>/materials/upload", methods=["GET", "POST"])
@login_required
@instructor_required
def upload_material_view(slug: str):
    course = get_course_by_slug(slug)
    if not course:
        abort(404)
    if not current_user.is_admin and course.instructor_id != current_user.id:
        abort(403)

    form = MaterialUploadForm()
    if form.validate_on_submit():
        upload_material(
            course=course,
            uploader_id=current_user.id,
            file=form.file.data,
            title=form.title.data,
            description=form.description.data or "",
            is_preview=form.is_preview.data,
        )
        flash("Material uploaded successfully.", "success")
        return redirect(url_for("courses.detail", slug=slug))

    return render_template(
        "courses/upload_material.html", form=form, course=course
    )


# ── Material delete ───────────────────────────────────────────────────────────

@courses_bp.route("/materials/<int:material_id>/delete", methods=["POST"])
@login_required
@instructor_required
def delete_material_view(material_id: int):
    from app.models.material import CourseMaterial
    material = CourseMaterial.query.get_or_404(material_id)
    course = material.course
    if not current_user.is_admin and course.instructor_id != current_user.id:
        abort(403)
    delete_material(material)
    flash("Material deleted.", "info")
    return redirect(url_for("courses.detail", slug=course.slug))
