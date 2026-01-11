from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class House(models.Model):

    HOUSE_TYPES = [
        ('1BHK', '1 BHK'),
        ('2BHK', '2 BHK'),
        ('3BHK', '3 BHK'),
        ('DUPLEX', 'Duplex'),
        ('VILLA', 'Villa'),
        ('BUNGALOW', 'Bungalow'),
        ('COMMERCIAL', 'Commercial'),
        ('CUSTOM', 'Custom'),
    ]

    name = models.CharField(max_length=100)
    house_type = models.CharField(max_length=20, choices=HOUSE_TYPES)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='houses/', blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    site_address = models.TextField()
    start_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def total_paid(self):
        return self.payments.aggregate(
            total=Sum('amount')
        )['total'] or 0

    def is_fully_paid(self):
        return self.total_paid() >= self.house.price

    def __str__(self):
        return f"{self.user.username} - {self.house.name}"


class Payment(models.Model):

    PAYMENT_TYPES = [
        ('Advance', 'Advance'),
        ('Full', 'Full'),
        ('Installment', 'Installment'),
    ]

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.PositiveIntegerField()
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    paid_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} (Booking {self.booking.id})"


class HouseImage(models.Model):
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='houses/gallery/')

    def __str__(self):
        return f"Image - {self.house.name}"
