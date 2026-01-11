from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Booking, Payment


@receiver(post_save, sender=Payment)
def update_booking_on_payment(sender, instance, created, **kwargs):
    if not created:
        return

    booking = instance.booking

    # Auto-complete booking if fully paid
    if booking.is_fully_paid():
        booking.status = 'COMPLETED'
        booking.save(update_fields=['status'])


@receiver(post_save, sender=Booking)
def booking_status_email(sender, instance, created, **kwargs):
    if created:
        return

    if not instance.user.email:
        return

    SUBJECT_MAP = {
        'APPROVED': 'Booking Approved',
        'CANCELLED': 'Booking Cancelled',
        'COMPLETED': 'Booking Completed'
    }

    if instance.status in SUBJECT_MAP:
        send_mail(
            subject=f"{SUBJECT_MAP[instance.status]} | MS Construction",
            message=(
                f"Hello {instance.user.username},\n\n"
                f"Booking for '{instance.house.name}' is now {instance.get_status_display()}.\n\n"
                f"Regards,\nMS Construction"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            fail_silently=True,
        )
