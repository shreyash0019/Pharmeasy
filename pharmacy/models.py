from django.db import models
from django.conf import settings

class MedicalStore(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=200)
    address = models.TextField()

class Medicine(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    requires_prescription = models.BooleanField(default=False)

class StoreInventory(models.Model):
    store = models.ForeignKey(MedicalStore, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()