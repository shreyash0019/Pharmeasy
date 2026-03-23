from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.utils import OperationalError

from .models import Medicine, StoreInventory, MedicalStore, Reminder
from orders.models import Order
from .serializers import (
    MedicineSerializer,
    StoreInventorySerializer,
    MedicalStoreSerializer,
    OrderSerializer,
    ReminderSerializer
)

# 💊 Medicines
class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]


# 🏪 Stores
class MedicalStoreViewSet(viewsets.ModelViewSet):
    queryset = MedicalStore.objects.all()
    serializer_class = MedicalStoreSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 📦 Inventory
class StoreInventoryViewSet(viewsets.ModelViewSet):
    queryset = StoreInventory.objects.select_related('store', 'medicine')
    serializer_class = StoreInventorySerializer
    permission_classes = [IsAuthenticated]


# 🔍 Search Medicines
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_medicine(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return Response({"error": "Please provide search query"}, status=400)

    try:
        inventories = StoreInventory.objects.select_related('medicine', 'store').filter(
            medicine__name__icontains=query,
            stock__gt=0
        ).order_by('price')
    except OperationalError:
        inventories = []

    result = []
    for item in inventories:
        result.append({
            "medicine": item.medicine.name,
            "store": item.store.store_name,
            "price": item.price,
            "stock": item.stock
        })

    return Response(result)


# 🛒 Orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user
    try:
        if hasattr(user, 'role') and user.role == "seller":
            orders = Order.objects.filter(store__user=user)
        else:
            orders = Order.objects.filter(patient=user)
    except OperationalError:
        orders = []

    return Response(OrderSerializer(orders, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(patient=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# 🏪 Stores
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stores(request):
    try:
        stores = MedicalStore.objects.all()
    except OperationalError:
        stores = []
    return Response(MedicalStoreSerializer(stores, many=True).data)


# ⏰ Reminders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reminders(request):
    try:
        reminders = Reminder.objects.filter(user=request.user)
    except OperationalError:
        reminders = []
    return Response(ReminderSerializer(reminders, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reminder(request):
    serializer = ReminderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
