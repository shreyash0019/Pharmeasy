from django.db import models
from django.conf import settings
from pharmacy.models import Medicine


class Reminder(models.Model):
    # 👤 User (patient)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_reminders"
    )

    # 💊 Medicine
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="medicine_reminders"
    )

    # ⏰ Time to take medicine
    reminder_time = models.TimeField()

    # 🔁 Frequency (times per day)
    frequency_per_day = models.PositiveIntegerField()

    # 📅 Start date
    start_date = models.DateField()

    # 📅 Optional end date
    end_date = models.DateField(null=True, blank=True)

    # ⏱️ Tracking
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.medicine.name}"
