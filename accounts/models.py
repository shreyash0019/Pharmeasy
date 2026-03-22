from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('seller', 'Seller'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # 🔔 FCM token for push notifications
    fcm_token = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
