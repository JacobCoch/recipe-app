from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import LoginForm, SignUpForm


class LoginFormTestCase(TestCase):
    def test_valid_login_form(self):
        form = LoginForm(data={"username": "testuser", "password": "testpass"})
        self.assertTrue(form.is_valid())

    def test_invalid_login_form_missing_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)

    def test_invalid_login_form_missing_username(self):
        form = LoginForm(data={"password": "testpass"})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_invalid_login_form_missing_password(self):
        form = LoginForm(data={"username": "testuser"})
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)


class SignUpFormTestCase(TestCase):
    def test_valid_signup_form(self):
        form = SignUpForm(
            data={
                "username": "newuser",
                "password": "newpass123",
                "confirm_password": "newpass123",
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_signup_form_password_mismatch(self):
        form = SignUpForm(
            data={
                "username": "newuser",
                "password": "newpass123",
                "confirm_password": "differentpass",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["__all__"], ["Passwords do not match"])

    def test_invalid_signup_form_missing_data(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)
        self.assertIn("confirm_password", form.errors)

    def test_invalid_signup_form_missing_username(self):
        form = SignUpForm(
            data={"password": "newpass123", "confirm_password": "newpass123"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
