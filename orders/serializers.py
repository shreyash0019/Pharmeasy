from rest_framework import serializers
from .models import Order, OrderItem


# 📦 Order Item Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'medicine',
            'medicine_name',
            'quantity'
        ]


# 🛒 Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'user_name',
            'store',
            'store_name',
            'status',
            'created_at',
            'items'
        ]

        read_only_fields = ['user', 'status']
