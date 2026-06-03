"""
tests/test_user_service.py
──────────────────────────
Tests for the user service layer.
"""
import pytest

from app.services.user_service import (
    InvalidRoleError,
    UserExistsError,
    authenticate,
    get_user_by_email,
    register_user,
)


class TestRegisterUser:
    def test_register_creates_user(self, app):
        with app.app_context():
            u = register_user("Alice", "Test", "alice@svc.test", "Test1234", "student")
            assert u.id is not None
            assert u.email == "alice@svc.test"
            assert u.role == "student"

    def test_password_is_hashed(self, app):
        with app.app_context():
            u = register_user("Bob", "Test", "bob@svc.test", "Test1234", "student")
            assert u.password_hash != "Test1234"
            assert u.check_password("Test1234")

    def test_email_normalised_to_lowercase(self, app):
        with app.app_context():
            u = register_user("Carol", "Test", "CAROL@SVC.TEST", "Test1234", "student")
            assert u.email == "carol@svc.test"

    def test_duplicate_email_raises(self, app):
        with app.app_context():
            register_user("Dave", "Test", "dave@svc.test", "Test1234", "student")
            with pytest.raises(UserExistsError):
                register_user("Dave2", "Test", "dave@svc.test", "Test1234", "student")

    def test_invalid_role_raises(self, app):
        with app.app_context():
            with pytest.raises(InvalidRoleError):
                register_user("Eve", "Test", "eve@svc.test", "Test1234", "superuser")


class TestAuthenticate:
    def test_valid_credentials_return_user(self, app):
        with app.app_context():
            register_user("Frank", "Test", "frank@svc.test", "Test1234", "student")
            u = authenticate("frank@svc.test", "Test1234")
            assert u is not None
            assert u.email == "frank@svc.test"

    def test_wrong_password_returns_none(self, app):
        with app.app_context():
            register_user("Grace", "Test", "grace@svc.test", "Test1234", "student")
            assert authenticate("grace@svc.test", "Wrong9999") is None

    def test_unknown_email_returns_none(self, app):
        with app.app_context():
            assert authenticate("nobody@svc.test", "Test1234") is None

    def test_inactive_user_cannot_login(self, app):
        with app.app_context():
            from app import db
            u = register_user("Henry", "Test", "henry@svc.test", "Test1234", "student")
            u.is_active = False
            db.session.commit()
            assert authenticate("henry@svc.test", "Test1234") is None


class TestGetUserByEmail:
    def test_found(self, app):
        with app.app_context():
            register_user("Iris", "Test", "iris@svc.test", "Test1234", "instructor")
            u = get_user_by_email("iris@svc.test")
            assert u is not None

    def test_not_found(self, app):
        with app.app_context():
            assert get_user_by_email("ghost@svc.test") is None
