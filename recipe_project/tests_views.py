from django.test import Client, TestCase
from django.urls import reverse

from recipes.models import CustomUser as User


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_login_view_with_valid_credentials(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpass"}
        )
        self.assertRedirects(response, reverse("recipes:home"))

    def test_login_view_with_invalid_credentials(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Oops, something went wrong.")


class SignupViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("signup")

    def test_signup_view_with_valid_data(self):
        data = {
            "username": "newuser",
            "password1": "newpass123",
            "password2": "newpass123",
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)

    def test_signup_view_with_invalid_data(self):
        data = {
            "username": "newuser",
            "password1": "newpass123",
            "password2": "differentpass",  # Passwords don't match
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Oops, something went wrong")
