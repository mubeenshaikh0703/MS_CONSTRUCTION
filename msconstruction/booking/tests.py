from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import House, Booking, Payment


class BookingFlowTest(TestCase):

    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

        # Create house
        self.house = House.objects.create(
            name='Test House',
            house_type='2BHK',
            description='Test Description',
            price=500000
        )

    def test_select_work_page_loads(self):
        response = self.client.get(reverse('select_work'))
        self.assertEqual(response.status_code, 200)

    def test_booking_creation(self):
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(
            reverse('booking', args=[self.house.id]),
            {
                'site_address': 'Test Address',
                'start_date': '2026-01-01'
            }
        )

        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.house, self.house)

    def test_payment_creation(self):
        self.client.login(username='testuser', password='testpass123')

        booking = Booking.objects.create(
            user=self.user,
            house=self.house,
            site_address='Test Address'
        )

        response = self.client.post(
            reverse('payment', args=[booking.id]),
            {
                'payment_type': 'Cash',
                'amount': 10000
            }
        )

        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.first()
        self.assertEqual(payment.booking, booking)

    def test_payment_history_page(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('payment_history'))
        self.assertEqual(response.status_code, 200)

    def test_cancel_booking(self):
        self.client.login(username='testuser', password='testpass123')

        booking = Booking.objects.create(
            user=self.user,
            house=self.house,
            site_address='Test Address'
        )

        response = self.client.post(
            reverse('cancel_booking', args=[booking.id])
        )

        booking.refresh_from_db()
        self.assertEqual(booking.status, 'CANCELLED')
