from django.db import models
from django.conf import settings

# 🏪 Medical Store
class MedicalStore(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medical_store"
    )
    store_name = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.store_name


# 💊 Medicine
class Medicine(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    requires_prescription = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# 📦 Store Inventory
class StoreInventory(models.Model):
    store = models.ForeignKey(
        MedicalStore,
        on_delete=models.CASCADE,
        related_name="inventories"
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="store_data"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    class Meta:
        unique_together = ['store', 'medicine']
        ordering = ['price']

    def __str__(self):
        return f"{self.store.store_name} - {self.medicine.name}"


# ⏰ Reminder
class Reminder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pharmacy_reminders"
    )
    message = models.TextField(null=True, blank=True)
    remind_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.message or "Reminder"
