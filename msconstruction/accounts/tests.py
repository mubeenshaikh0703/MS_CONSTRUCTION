from django.test import TestCase
from django.contrib.auth.models import User


class AccountsTests(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertTrue(user.check_password('testpass123'))

    def test_login_page_loads(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_loads(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_reset_password_page_loads(self):
        response = self.client.get('/reset-password/')
        self.assertEqual(response.status_code, 200)
