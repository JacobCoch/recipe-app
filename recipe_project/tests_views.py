from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_login_view_with_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertRedirects(response, reverse('recipes:recipes'))

    def test_login_view_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ooops.. something went wrong')