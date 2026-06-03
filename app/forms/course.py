"""
app/forms/course.py
───────────────────
WTForms for creating/editing courses and uploading materials.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    BooleanField, DecimalField, IntegerField, SelectField,
    StringField, SubmitField, TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.models.course import Course

ALLOWED_MATERIAL_TYPES = ["pdf", "png", "jpg", "jpeg", "gif", "mp4", "zip", "docx", "pptx"]


class CourseForm(FlaskForm):
    title = StringField(
        "Course Title",
        validators=[DataRequired(), Length(min=5, max=200)],
    )
    short_description = StringField(
        "Short Description (shown on cards)",
        validators=[DataRequired(), Length(max=300)],
    )
    description = TextAreaField(
        "Full Description",
        validators=[DataRequired(), Length(min=20)],
    )
    level = SelectField(
        "Difficulty Level",
        choices=[(lvl, lvl) for lvl in Course.LEVELS],
    )
    duration_hours = IntegerField(
        "Estimated Duration (hours)",
        validators=[Optional(), NumberRange(min=0, max=9999)],
        default=0,
    )
    price = DecimalField(
        "Price (0 = Free)",
        validators=[Optional(), NumberRange(min=0)],
        places=2,
        default=0.00,
    )
    category_id = SelectField("Category", coerce=int, validators=[Optional()])
    thumbnail_url = StringField(
        "Thumbnail Image URL (optional)",
        validators=[Optional(), Length(max=512)],
    )
    is_published = BooleanField("Publish immediately")
    submit = SubmitField("Save Course")


class MaterialUploadForm(FlaskForm):
    title = StringField(
        "Material Title",
        validators=[DataRequired(), Length(min=2, max=200)],
    )
    description = TextAreaField(
        "Description (optional)",
        validators=[Optional(), Length(max=500)],
    )
    file = FileField(
        "File",
        validators=[
            FileRequired(),
            FileAllowed(ALLOWED_MATERIAL_TYPES, "File type not allowed."),
        ],
    )
    is_preview = BooleanField("Allow preview (visible without enrollment)")
    submit = SubmitField("Upload Material")


class CourseSearchForm(FlaskForm):
    """Lightweight search/filter form (no CSRF needed for GET)."""
    class Meta:
        csrf = False

    q = StringField("Search", validators=[Optional(), Length(max=100)])
    level = SelectField(
        "Level",
        choices=[("", "All Levels")] + [(lvl, lvl) for lvl in Course.LEVELS],
        validators=[Optional()],
    )
    category = SelectField("Category", coerce=int, validators=[Optional()])
    submit = SubmitField("Search")
