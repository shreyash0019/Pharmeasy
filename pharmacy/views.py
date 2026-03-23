# pharmacy/views.py
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


# 💊 Medicines — all users can see all
class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]


# 🏪 Stores — all users can see all
class MedicalStoreViewSet(viewsets.ModelViewSet):
    queryset = MedicalStore.objects.all()
    serializer_class = MedicalStoreSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 📦 Inventory — all users can see all
class StoreInventoryViewSet(viewsets.ModelViewSet):
    queryset = StoreInventory.objects.select_related('store', 'medicine').all()
    serializer_class = StoreInventorySerializer
    permission_classes = [IsAuthenticated]


# 🔍 Search Medicines — global search
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_medicine(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return Response({"error": "Please provide search query"}, status=400)

    try:
        inventories = StoreInventory.objects.select_related('medicine', 'store').filter(
            Q(medicine__name__icontains=query) |
            Q(medicine__description__icontains=query)
        ).order_by('price')
    except OperationalError:
        inventories = []

    # Group by medicine
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


# 🛒 Get Orders — seller sees their store orders, others see patient orders
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


# 🛒 Create Order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(patient=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# 🏪 Get Stores — all stores
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stores(request):
    try:
        stores = MedicalStore.objects.all()
    except OperationalError:
        stores = []
    return Response(MedicalStoreSerializer(stores, many=True).data)


# ⏰ Get Reminders — only user's reminders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reminders(request):
    try:
        reminders = Reminder.objects.filter(user=request.user)
    except OperationalError:
        reminders = []
    return Response(ReminderSerializer(reminders, many=True).data)


# ⏰ Create Reminder — attach user automatically
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reminder(request):
    serializer = ReminderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
