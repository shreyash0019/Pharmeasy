from django.db import models
from django.conf import settings
from pharmacy.models import Medicine, MedicalStore

class Order(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.ForeignKey(MedicalStore, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    # ⚠️ Removed updated_at for Render free

    def __str__(self):
        return f"Order #{self.id} by {self.patient.username}"
