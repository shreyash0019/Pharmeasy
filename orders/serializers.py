```python
from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    # 🔹 Readable fields for frontend
    patient_name = serializers.CharField(source='patient.username', read_only=True)
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    # 🔹 Optional: full URLs for prescription file
    prescription = serializers.FileField(required=False, allow_null=True)

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

        read_only_fields = [
            'patient',
            'status',
            'created_at'
        ]

    # 🔥 Auto-assign logged-in user as patient
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['patient'] = request.user
        return super().create(validated_data)

    # 🔥 Optional: update restriction (only allow quantity/prescription change)
    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.prescription = validated_data.get('prescription', instance.prescription)
        instance.save()
        return instance
```
