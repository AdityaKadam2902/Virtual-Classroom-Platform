
# 🎓 LearnHub — Virtual Classroom & Learning Platform

> A modern, scalable, and production-ready Learning Management System (LMS) built using Flask, SQLAlchemy, Bootstrap 5, and modern software engineering practices.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![License](https://img.shields.io/badge/Status-Completed-success)

---

## 📌 Project Overview

**LearnHub** is a full-featured virtual classroom platform designed to bridge the gap between educators and learners through an intuitive digital learning environment.

The platform enables instructors to create and manage courses, students to enroll and access learning materials, and administrators to oversee the entire ecosystem through a dedicated management portal.

Built with scalability, security, maintainability, and clean architecture principles in mind, LearnHub demonstrates industry-level backend development practices and modern web application design.

---

## 🚀 Key Features

### 👨‍🎓 Student Portal

* User registration and authentication
* Browse available courses
* Course enrollment system
* Access learning materials
* Personalized dashboard
* Progress tracking

### 👨‍🏫 Instructor Portal

* Create and manage courses
* Upload educational content
* Monitor student enrollments
* Manage course lifecycle
* Course publishing controls

### 👨‍💼 Administrator Portal

* User management
* Course moderation
* Category management
* Platform oversight
* Content approval workflows

### 🔒 Security Features

* Secure Authentication
* Password Hashing
* CSRF Protection
* Input Validation
* Environment-based Configuration
* Role-Based Access Control (RBAC)

### 📂 Learning Resources

* PDF Upload Support
* Video Upload Support
* Image Upload Support
* Archive/File Attachments
* Local Storage Support
* AWS S3 Integration

---

## 🏗️ System Architecture

The application follows a clean and maintainable layered architecture:

Presentation Layer
│
├── Jinja2 Templates
├── Bootstrap 5 UI
└── Static Assets (CSS/JS)
        │
        ▼
Application Layer
│
├── Flask Blueprints
│   ├── Auth Module
│   ├── Course Module
│   ├── Dashboard Module
│   └── Admin Module
│
├── WTForms Validation
└── Utility Components
        │
        ▼
Business Layer
│
├── User Service
├── Course Service
└── Storage Service
        │
        ▼
Data Access Layer
│
└── SQLAlchemy ORM Models
    ├── User
    ├── Course
    ├── Enrollment
    └── Material
        │
        ▼
Persistence Layer
│
├── SQLite (Development)
├── PostgreSQL (Production)
└── MySQL (Supported)

### Architecture Highlights

✅ Application Factory Pattern

✅ Blueprint-Based Modular Structure

✅ Service-Oriented Business Logic

✅ Environment-Based Configuration

✅ Storage Abstraction Layer

✅ Scalable Database Design

✅ Testable Codebase

---

## 🛠️ Technology Stack

### Backend

* Python
* Flask
* SQLAlchemy
* WTForms
* Jinja2

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

### Database

* SQLite (Development)
* PostgreSQL (Production Ready)
* MySQL Supported

### Cloud & Storage

* AWS S3
* Local File Storage

### Testing

* Pytest

---

## 📂 Project Structure

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

---

## ⚡ Quick Start

### Clone Repository

```bash
git clone https://github.com/yourusername/learnhub.git
cd learnhub
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / MacOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

```bash
cp .env.example .env
```

Update the required values inside the `.env` file.

### Initialize Database

```bash
flask db upgrade
```

### Run Application

```bash
python run.py
```

Application will be available at:

```text
http://localhost:5000
```

---

## 🧪 Testing

Run all tests:

```bash
pytest
```

Run with detailed output:

```bash
pytest -v
```

---

## 📈 Production Readiness

The platform is designed with production deployment in mind:

* Environment-based configuration
* Secure credential management
* Database migration support
* Cloud storage integration
* Scalable architecture
* Role-based authorization
* Service-layer abstraction
* Automated testing support

---

## 🎯 Software Engineering Practices Demonstrated

* Object-Oriented Programming (OOP)
* MVC-inspired Architecture
* Design Patterns
* Separation of Concerns
* Modular Development
* RESTful Principles
* Secure Coding Practices
* Database Modeling
* Automated Testing
* Clean Code Standards

---

## 💡 Future Enhancements

* Live Video Classes
* AI-Powered Learning Assistant
* Course Completion Certificates
* Assignment Submission System
* Online Examination Module
* Discussion Forums
* Real-Time Notifications
* Mobile Application
* Analytics Dashboard
* Multi-Language Support

---

## 👨‍💻 Developer

### Aditya Kadam

Software Developer | Python Developer | AI & Full-Stack Enthusiast

Passionate about building scalable software solutions, AI-powered applications, automation systems, and modern web platforms.

**Core Interests**

* Python Development
* Artificial Intelligence
* Backend Engineering
* Cloud Computing
* Software Architecture
* Automation Systems

---

## ⭐ Why This Project Matters

LearnHub showcases the ability to design, develop, test, and deploy a complete production-grade web application while following industry best practices in software engineering, security, scalability, and maintainability.

This project demonstrates skills highly relevant to:

* Software Development Engineer (SDE)
* Python Developer
* Backend Developer
* Full Stack Developer
* Software Engineer
* AI Application Developer

---

### 🌟 If you found this project valuable, consider giving it a Star!
