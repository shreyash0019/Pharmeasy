from django.db import models
from django.conf import settings
from pharmacy.models import Medicine, MedicalStore


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    # 👤 Patient (user placing order)
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_orders"
    )

    # 🏪 Store fulfilling order
    store = models.ForeignKey(
        MedicalStore,
        on_delete=models.CASCADE,
        related_name="store_orders"
    )

    # 💊 Medicine
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="medicine_orders"
    )

    # 🔢 Quantity
    quantity = models.PositiveIntegerField()

    # 📄 Prescription (optional)
    prescription = models.FileField(
        upload_to='prescriptions/',
        null=True,
        blank=True
    )

    # 📦 Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # ⏱️ Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.patient.username} - {self.status}"
