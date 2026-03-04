from rest_framework import serializers
from .models import Medicine, StoreInventory, MedicalStore


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


class MedicalStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalStore
        fields = '__all__'
        read_only_fields = ['user']


class StoreInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        fields = '__all__'