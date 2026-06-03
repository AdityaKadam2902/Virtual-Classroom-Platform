"""
scripts/seed.py
───────────────
Populate the database with sample data for development / demo.

Usage:
    flask shell
    >>> exec(open('scripts/seed.py').read())

Or via CLI (after `flask db upgrade`):
    python scripts/seed.py
"""
import sys
import os

# Allow running directly: python scripts/seed.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.user import User, ROLE_ADMIN, ROLE_INSTRUCTOR, ROLE_STUDENT
from app.models.course import Category, Course
from app.models.enrollment import Enrollment

app = create_app()

CATEGORIES = [
    {"name": "Web Development",     "slug": "web-development",     "icon": "bi-globe"},
    {"name": "Data Science",        "slug": "data-science",        "icon": "bi-graph-up"},
    {"name": "Machine Learning",    "slug": "machine-learning",    "icon": "bi-cpu"},
    {"name": "Mobile Development",  "slug": "mobile-development",  "icon": "bi-phone"},
    {"name": "Cybersecurity",       "slug": "cybersecurity",       "icon": "bi-shield-lock"},
    {"name": "Cloud Computing",     "slug": "cloud-computing",     "icon": "bi-cloud"},
    {"name": "DevOps",              "slug": "devops",              "icon": "bi-gear"},
    {"name": "UI/UX Design",        "slug": "ui-ux-design",        "icon": "bi-palette"},
]

USERS = [
    {
        "first_name": "Alice",  "last_name": "Admin",
        "email": "admin@learnhub.dev",  "password": "Admin1234",
        "role": ROLE_ADMIN,
    },
    {
        "first_name": "Ivan",   "last_name": "Instructor",
        "email": "instructor@learnhub.dev",  "password": "Teach1234",
        "role": ROLE_INSTRUCTOR,
    },
    {
        "first_name": "Sara",   "last_name": "Instructor",
        "email": "sara@learnhub.dev",  "password": "Teach1234",
        "role": ROLE_INSTRUCTOR,
    },
    {
        "first_name": "Bob",    "last_name": "Student",
        "email": "student@learnhub.dev",  "password": "Learn1234",
        "role": ROLE_STUDENT,
    },
    {
        "first_name": "Clara",  "last_name": "Student",
        "email": "clara@learnhub.dev",  "password": "Learn1234",
        "role": ROLE_STUDENT,
    },
]

COURSES = [
    {
        "title": "The Complete Python Bootcamp",
        "slug": "complete-python-bootcamp",
        "short_description": "Go from zero to hero in Python with hands-on projects and real-world examples.",
        "description": (
            "This comprehensive Python course takes you from the very basics all the way to "
            "advanced topics including OOP, file I/O, web scraping, and automation. "
            "You will build 10+ real-world projects and finish with a solid portfolio piece. "
            "No prior programming experience required."
        ),
        "level": "Beginner",
        "duration_hours": 42,
        "price": 0.00,
        "category_slug": "web-development",
        "is_published": True,
        "instructor_email": "instructor@learnhub.dev",
        "thumbnail_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=600&q=80",
    },
    {
        "title": "Machine Learning A–Z",
        "slug": "machine-learning-a-z",
        "short_description": "Master supervised and unsupervised learning, neural networks, and model deployment.",
        "description": (
            "Learn machine learning from scratch using Python, Scikit-learn, and TensorFlow. "
            "Cover regression, classification, clustering, deep learning, and how to deploy "
            "models to production. Includes 50+ hands-on exercises and a capstone project."
        ),
        "level": "Intermediate",
        "duration_hours": 60,
        "price": 29.99,
        "category_slug": "machine-learning",
        "is_published": True,
        "instructor_email": "sara@learnhub.dev",
        "thumbnail_url": "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=600&q=80",
    },
    {
        "title": "React & Node.js Full-Stack Development",
        "slug": "react-nodejs-fullstack",
        "short_description": "Build production-ready full-stack web apps with React, Node.js, and MongoDB.",
        "description": (
            "Learn to build modern, scalable web applications from the ground up. "
            "This course covers React hooks, Redux, REST APIs with Express, MongoDB with Mongoose, "
            "JWT authentication, and deployment to AWS. Perfect for developers looking to go full-stack."
        ),
        "level": "Intermediate",
        "duration_hours": 55,
        "price": 24.99,
        "category_slug": "web-development",
        "is_published": True,
        "instructor_email": "instructor@learnhub.dev",
        "thumbnail_url": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=600&q=80",
    },
    {
        "title": "Cybersecurity Fundamentals",
        "slug": "cybersecurity-fundamentals",
        "short_description": "Understand network security, ethical hacking basics, and how to protect systems.",
        "description": (
            "This course gives you a solid foundation in cybersecurity. Topics include "
            "network protocols, common attack vectors (SQL injection, XSS, MITM), "
            "encryption, firewalls, and security best practices. Hands-on labs in a safe environment."
        ),
        "level": "Beginner",
        "duration_hours": 30,
        "price": 0.00,
        "category_slug": "cybersecurity",
        "is_published": True,
        "instructor_email": "sara@learnhub.dev",
        "thumbnail_url": "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=600&q=80",
    },
    {
        "title": "Advanced Data Science with Python",
        "slug": "advanced-data-science-python",
        "short_description": "Deep dive into Pandas, NumPy, data visualization, and statistical analysis.",
        "description": (
            "Take your data skills to the next level. Master Pandas for data wrangling, "
            "Matplotlib and Seaborn for visualization, hypothesis testing, time-series analysis, "
            "and building interactive dashboards with Plotly. Ideal for analysts and engineers."
        ),
        "level": "Advanced",
        "duration_hours": 48,
        "price": 34.99,
        "category_slug": "data-science",
        "is_published": True,
        "instructor_email": "instructor@learnhub.dev",
        "thumbnail_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=80",
    },
    {
        "title": "DevOps with Docker & Kubernetes",
        "slug": "devops-docker-kubernetes",
        "short_description": "Containerise applications and orchestrate at scale with Docker and Kubernetes.",
        "description": (
            "Go from Docker basics to running a production Kubernetes cluster on the cloud. "
            "Learn container networking, persistent storage, Helm charts, CI/CD pipelines, "
            "and monitoring with Prometheus and Grafana."
        ),
        "level": "Advanced",
        "duration_hours": 40,
        "price": 19.99,
        "category_slug": "devops",
        "is_published": True,
        "instructor_email": "sara@learnhub.dev",
        "thumbnail_url": "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=600&q=80",
    },
    {
        "title": "UI/UX Design Masterclass",
        "slug": "ui-ux-design-masterclass",
        "short_description": "Learn Figma, design systems, user research, and prototyping from scratch.",
        "description": (
            "A comprehensive guide to modern product design. Starting with user research and "
            "wireframing, through high-fidelity prototypes in Figma, to design systems and "
            "handoff to developers. Includes 12 real-world design challenges."
        ),
        "level": "Beginner",
        "duration_hours": 35,
        "price": 0.00,
        "category_slug": "ui-ux-design",
        "is_published": True,
        "instructor_email": "instructor@learnhub.dev",
        "thumbnail_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=600&q=80",
    },
    # Draft course — not visible to students
    {
        "title": "Cloud Architecture on AWS (Coming Soon)",
        "slug": "cloud-architecture-aws",
        "short_description": "Design and deploy scalable, fault-tolerant architectures on AWS.",
        "description": "Draft — not yet published.",
        "level": "Advanced",
        "duration_hours": 50,
        "price": 39.99,
        "category_slug": "cloud-computing",
        "is_published": False,
        "instructor_email": "sara@learnhub.dev",
        "thumbnail_url": "",
    },
]


def run():
    with app.app_context():
        print("🌱  Starting seed…")

        # Wipe and recreate tables
        db.drop_all()
        db.create_all()

        # ── Categories ────────────────────────────────────────────
        cat_map = {}
        for data in CATEGORIES:
            cat = Category(**data)
            db.session.add(cat)
            cat_map[data["slug"]] = cat
        db.session.flush()
        print(f"  ✓ {len(CATEGORIES)} categories")

        # ── Users ─────────────────────────────────────────────────
        user_map = {}
        for data in USERS:
            u = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                role=data["role"],
            )
            u.set_password(data["password"])
            db.session.add(u)
            user_map[data["email"]] = u
        db.session.flush()
        print(f"  ✓ {len(USERS)} users")

        # ── Courses ───────────────────────────────────────────────
        course_map = {}
        for data in COURSES:
            cat = cat_map.get(data.pop("category_slug"))
            instructor = user_map[data.pop("instructor_email")]
            c = Course(
                instructor_id=instructor.id,
                category_id=cat.id if cat else None,
                **data,
            )
            db.session.add(c)
            course_map[c.slug] = c
        db.session.flush()
        print(f"  ✓ {len(COURSES)} courses")

        # ── Enrollments ───────────────────────────────────────────
        enrollments = [
            ("student@learnhub.dev", "complete-python-bootcamp"),
            ("student@learnhub.dev", "cybersecurity-fundamentals"),
            ("student@learnhub.dev", "ui-ux-design-masterclass"),
            ("clara@learnhub.dev",   "complete-python-bootcamp"),
            ("clara@learnhub.dev",   "machine-learning-a-z"),
        ]
        for email, slug in enrollments:
            e = Enrollment(
                student_id=user_map[email].id,
                course_id=course_map[slug].id,
                progress=int(hash(email + slug) % 101),
            )
            db.session.add(e)
        print(f"  ✓ {len(enrollments)} enrollments")

        db.session.commit()
        print()
        print("✅  Seed complete!")
        print()
        print("  Demo accounts")
        print("  ─────────────────────────────────────────")
        for u in USERS:
            print(f"  {u['role']:12s}  {u['email']:35s}  pw: {u['password']}")
        print()


if __name__ == "__main__":
    run()
