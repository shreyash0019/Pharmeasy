from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.username', read_only=True)
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'patient',
            'patient_name',
            'store',
            'store_name',
            'medicine',
            'medicine_name',
            'quantity',
            'prescription',
            'status',
            'created_at'
        ]

        read_only_fields = ['patient', 'status']
