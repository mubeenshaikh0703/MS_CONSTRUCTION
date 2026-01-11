from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_photo = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.png',
        blank=True
    )

    phone = models.CharField(max_length=15)
    middle_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username
