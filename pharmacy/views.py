from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Medicine, StoreInventory, MedicalStore, Reminder
from orders.models import Order

from .serializers import (
    MedicineSerializer,
    StoreInventorySerializer,
    MedicalStoreSerializer,
    OrderSerializer,
    ReminderSerializer
)


# 💊 MEDICINE
class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]


# 🏪 STORE
class MedicalStoreViewSet(viewsets.ModelViewSet):
    queryset = MedicalStore.objects.all()
    serializer_class = MedicalStoreSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 📦 INVENTORY
class StoreInventoryViewSet(viewsets.ModelViewSet):
    queryset = StoreInventory.objects.select_related('store', 'medicine')
    serializer_class = StoreInventorySerializer
    permission_classes = [IsAuthenticated]


# 🔍 SEARCH (FIXED + OPTIMIZED)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_medicine(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return Response({"error": "Please provide search query"}, status=400)

    inventories = StoreInventory.objects.select_related('medicine', 'store').filter(
        Q(medicine__name__icontains=query),
        stock__gt=0
    ).order_by('price')  # 🔥 cheapest first

    result = {}

    for item in inventories:
        med_id = item.medicine.id

        if med_id not in result:
            result[med_id] = {
                "medicine_id": med_id,
                "medicine": item.medicine.name,
                "description": item.medicine.description,
                "requires_prescription": item.medicine.requires_prescription,
                "stores": []
            }

        result[med_id]["stores"].append({
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


# 🛒 CREATE ORDER
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(patient=request.user)
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


# ⏰ CREATE REMINDER
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reminder(request):
    serializer = ReminderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
