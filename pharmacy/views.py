from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import datetime

from .models import Medicine, StoreInventory, MedicalStore, Reminder
from orders.models import Order

from .serializers import (
    MedicineSerializer,
    StoreInventorySerializer,
    MedicalStoreSerializer,
    OrderSerializer,
    ReminderSerializer
)

# 💊 MEDICINE (ALL USERS CAN SEE ALL MEDICINES)
class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]


# 🏪 STORE (ALL USERS CAN SEE ALL STORES)
class MedicalStoreViewSet(viewsets.ModelViewSet):
    queryset = MedicalStore.objects.all()
    serializer_class = MedicalStoreSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 📦 INVENTORY (ALL USERS CAN SEE ALL INVENTORY)
class StoreInventoryViewSet(viewsets.ModelViewSet):
    queryset = StoreInventory.objects.select_related('store', 'medicine').all()
    serializer_class = StoreInventorySerializer
    permission_classes = [IsAuthenticated]


# 🔍 SEARCH (MAIN FEATURE — WORKS LIKE PHARMACY APP)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_medicine(request):
    query = request.GET.get('q', '')

    if not query:
        return Response({"error": "Please provide search query"}, status=400)

    inventories = StoreInventory.objects.select_related('medicine', 'store').filter(
        Q(medicine__name__icontains=query),
        stock__gt=0,
        expiry_date__gt=datetime.now()
    )

    result = {}

    for item in inventories:
        med_name = item.medicine.name

        if med_name not in result:
            result[med_name] = {
                "medicine_id": item.medicine.id,
                "medicine": med_name,
                "description": item.medicine.description,
                "requires_prescription": item.medicine.requires_prescription,
                "stores": []
            }

        result[med_name]["stores"].append({
            "store_id": item.store.id,
            "store_name": item.store.store_name,
            "price": item.price,
            "stock": item.stock
        })

    return Response(list(result.values()))


# 🛒 GET ORDERS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user

    if hasattr(user, 'role') and user.role == "seller":
        orders = Order.objects.filter(store__user=user)
    else:
        orders = Order.objects.filter(patient=user)

    return Response(OrderSerializer(orders, many=True).data)


# 🛒 CREATE ORDER ✅ (ADDED — IMPORTANT)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(patient=request.user)  # 🔥 attach user
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# 🏪 GET STORES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stores(request):
    stores = MedicalStore.objects.all()
    return Response(MedicalStoreSerializer(stores, many=True).data)


# ⏰ GET REMINDERS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reminders(request):
    reminders = Reminder.objects.filter(user=request.user)
    return Response(ReminderSerializer(reminders, many=True).data)


# ⏰ CREATE REMINDER ✅ (FIXED)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reminder(request):
    serializer = ReminderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # 🔥 IMPORTANT FIX
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
