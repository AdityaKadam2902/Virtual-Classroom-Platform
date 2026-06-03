# LearnHub — Virtual Classroom & Learning Platform

A production-ready virtual classroom platform built with Flask, SQLAlchemy, and Bootstrap 5.

---

## Features

- **Multi-role auth** — Student, Instructor, and Admin roles with secure session management
- **Course lifecycle** — Create, edit, publish, search, and filter courses
- **Enrollment** — Students enrol in courses; instructors see their student counts
- **File uploads** — Upload PDFs, videos, images, and archives per course; switchable local / AWS S3 storage
- **Admin panel** — Manage users, toggle publish status, manage categories
- **Secure by default** — No hardcoded secrets, CSRF protection, hashed passwords, input validation
- **35 passing tests** — Auth, course, and service-layer coverage

---

## Project Structure

```
learnhub/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Environment-based config
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   └── material.py
│   ├── routes/              # Flask blueprints
│   │   ├── main.py          # Home, About
│   │   ├── auth.py          # Register, Login, Logout
│   │   ├── courses.py       # Course CRUD, enrollment, materials
│   │   ├── dashboard.py     # Student & instructor dashboards
│   │   └── admin.py         # Admin panel
│   ├── services/            # Business logic layer
│   │   ├── course_service.py
│   │   ├── user_service.py
│   │   └── storage.py       # Local / S3 abstraction
│   ├── forms/               # WTForms with server-side validation
│   │   ├── auth.py
│   │   └── course.py
│   ├── utils/
│   │   ├── decorators.py    # @instructor_required, @admin_required
│   │   └── template_helpers.py
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, JS
├── scripts/
│   └── seed.py              # Demo data seeder
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_courses.py
│   └── test_user_service.py
├── run.py                   # Dev server entry point
├── manage.py                # Flask CLI helpers
├── requirements.txt
├── .env.example
└── pytest.ini
```

---

## Quick Start

### 1. Clone & set up environment

```bash
git clone <repo-url> learnhub
cd learnhub
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env — at minimum set a SECRET_KEY
```

For local development the SQLite default requires no further setup.

### 3. Initialise the database

```bash
# Option A — Flask-Migrate (recommended, preserves data across schema changes)
flask db init
flask db migrate -m "initial schema"
flask db upgrade

# Option B — quick reset (dev only)
flask init-db
```

### 4. Seed demo data (optional)

```bash
python scripts/seed.py
```

Demo accounts created:

| Role       | Email                    | Password   |
|------------|--------------------------|------------|
| Admin      | admin@learnhub.dev       | Admin1234  |
| Instructor | instructor@learnhub.dev  | Teach1234  |
| Instructor | sara@learnhub.dev        | Teach1234  |
| Student    | student@learnhub.dev     | Learn1234  |
| Student    | clara@learnhub.dev       | Learn1234  |

### 5. Run

```bash
python run.py
# → http://localhost:5000
```

---

## Running Tests

```bash
FLASK_ENV=testing pytest
# or with coverage:
FLASK_ENV=testing pytest --tb=short -v
```

---

## Production Deployment

### Environment variables required

| Variable              | Description                               |
|-----------------------|-------------------------------------------|
| `SECRET_KEY`          | Long random string — never commit this    |
| `DATABASE_URL`        | PostgreSQL or MySQL connection string     |
| `STORAGE_BACKEND`     | `s3` for AWS, `local` for filesystem      |
| `AWS_ACCESS_KEY_ID`   | Required when `STORAGE_BACKEND=s3`        |
| `AWS_SECRET_ACCESS_KEY` | Required when `STORAGE_BACKEND=s3`      |
| `AWS_S3_BUCKET`       | S3 bucket name                            |
| `AWS_S3_REGION`       | e.g. `us-east-1`                          |
| `FLASK_ENV`           | Set to `production`                       |

### Gunicorn

```bash
gunicorn "run:app" --workers 4 --bind 0.0.0.0:8000
```

---

## Architecture Decisions

- **Application factory** (`create_app`) — enables multiple configs (dev/test/prod) and clean testing.
- **Blueprints** — each feature area is an isolated blueprint; easy to add new ones.
- **Service layer** — `services/` contains all business logic; routes stay thin.
- **Storage abstraction** — `LocalStorage` and `S3Storage` share the same interface. Swap via env var, no code changes needed.
- **WTForms** — all user input validated server-side before hitting the service layer.
- **CSRF** — Flask-WTF protects all state-changing forms.

---

## Extending the Platform

- **Add a new role**: extend `VALID_ROLES` in `app/models/user.py` and add a decorator in `app/utils/decorators.py`.
- **Add a new feature (e.g. Reviews)**: create `app/models/review.py`, add to `app/models/__init__.py`, create `app/services/review_service.py`, add blueprint in `app/routes/review.py`, register in `app/__init__.py`.
- **Switch to PostgreSQL**: update `DATABASE_URL` in `.env` — no code changes needed.
- **Email support**: configure `MAIL_*` env vars and integrate Flask-Mail in `app/services/`.
