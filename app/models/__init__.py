# Import every model here so Flask-Migrate / Alembic detects them
# when it inspects SQLAlchemy metadata at migration time.
from app.models.user import User          # noqa: F401
from app.models.course import Category, Course, Tag   # noqa: F401
from app.models.enrollment import Enrollment           # noqa: F401
from app.models.material import CourseMaterial         # noqa: F401
