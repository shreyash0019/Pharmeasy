from django.db import models
from django.conf import settings
from pharmacy.models import Medicine

class Reminder(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    time = models.TimeField()
    frequency_per_day = models.IntegerField()
    start_date = models.DateField()