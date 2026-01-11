from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ContactMessage


class HomePageTest(TestCase):

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_contact_form_submission(self):
        response = self.client.post(reverse('home'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Hello MS Construction'
        })
        self.assertEqual(ContactMessage.objects.count(), 1)


class AdminDashboardTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )

    def test_admin_dashboard_access(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
