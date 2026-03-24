from rest_framework import serializers
from .models import Medicine, StoreInventory, MedicalStore, Reminder
from orders.models import Order

# 💊 Medicine
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id','name','description','requires_prescription']

# 🏪 Medical Store
class MedicalStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalStore
        fields = ['id','store_name','address']

# 📦 Store Inventory
class StoreInventorySerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = StoreInventory
        fields = ['id','store','store_name','medicine','medicine_name','price','stock']

# 🛒 Order
class OrderSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id','store','store_name','medicine','medicine_name','quantity','status','created_at']

# ⏰ Reminder
class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id','message','remind_at']
