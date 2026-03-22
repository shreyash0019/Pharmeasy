from django.db import models
from django.conf import settings


# 🏪 Medical Store
class MedicalStore(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medical_store"   # ✅ added
    )
    store_name = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.store_name


# 💊 Medicine Master
class Medicine(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    requires_prescription = models.BooleanField(default=False)

    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    composition = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


# 📦 Store Inventory
class StoreInventory(models.Model):
    store = models.ForeignKey(
        MedicalStore,
        on_delete=models.CASCADE,
        related_name="inventories"   # ✅ added
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="store_data"   # ✅ added
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    expiry_date = models.DateField(null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ['store', 'medicine']

    def __str__(self):
        return f"{self.store.store_name} - {self.medicine.name}"


# 🛒 Orders
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pharmacy_orders"   # ✅ FIXED
    )
    store = models.ForeignKey(
        MedicalStore,
        on_delete=models.CASCADE,
        related_name="store_orders"   # ✅ FIXED
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


# 📦 Order Items
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="order_items"   # ✅ added
    )
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"


# ⏰ Reminders
class Reminder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pharmacy_reminders"   # ✅ FIXED
    )
    message = models.TextField()
    remind_at = models.DateTimeField()

    def __str__(self):
        return self.message
