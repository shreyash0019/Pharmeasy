from rest_framework import serializers
from .models import Medicine, StoreInventory, MedicalStore


# 💊 Medicine Serializer
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = [
            'id',
            'name',
            'description',
            'requires_prescription',
            'manufacturer',
            'composition'
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


# 📦 Store Inventory Serializer (IMPORTANT UPGRADE)
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
