from rest_framework import serializers
from .models import Medicine, StoreInventory, MedicalStore, Reminder
from orders.models import Order

# 💊 Medicine Serializer (NO manufacturer/composition)
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = [
            'id',
            'name',
            'description',
            'requires_prescription'
        ]


# 🏪 Medical Store Serializer
class MedicalStoreSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MedicalStore
        fields = [
            'id',
            'store_name',
            'address',
            'user'
        ]


# 📦 Store Inventory Serializer
class StoreInventorySerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = StoreInventory
        fields = [
            'id',
            'store',
            'store_name',
            'medicine',
            'medicine_name',
            'price',
            'discount_price',
            'stock',
            'expiry_date'
        ]


# 🛒 Order Serializer (IMPORTANT FIX)
class OrderSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    patient_name = serializers.CharField(source='patient.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'store',
            'store_name',
            'medicine',
            'medicine_name',
            'patient',
            'patient_name',
            'quantity',
            'status',
            'created_at'
        ]


# ⏰ Reminder Serializer
class ReminderSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Reminder
        fields = [
            'id',
            'medicine',
            'medicine_name',
            'user',
            'user_name',
            'reminder_time',
            'frequency_per_day',
            'start_date',
            'end_date'
        ]
