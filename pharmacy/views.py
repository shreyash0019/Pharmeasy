from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import (
    Medicine,
    StoreInventory,
    MedicalStore,
    Order,
    Reminder
)

from .serializers import (
    MedicineSerializer,
    StoreInventorySerializer,
    MedicalStoreSerializer,
    OrderSerializer,
    ReminderSerializer
)


# 🔹 MEDICINE CRUD
class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]


# 🔹 MEDICAL STORE CRUD
class MedicalStoreViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalStoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # ✅ seller sees only his store
        if hasattr(user, 'medical_store'):
            return MedicalStore.objects.filter(user=user)

        return MedicalStore.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 🔹 STORE INVENTORY CRUD
class StoreInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = StoreInventorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # ✅ seller sees only his inventory
        if hasattr(user, 'medical_store'):
            return StoreInventory.objects.filter(store__user=user)

        return StoreInventory.objects.all()


# 🔍 SEARCH MEDICINE (FIXED + IMPROVED)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_medicine(request):
    query = request.GET.get('q', '')

    if not query:
        return Response({"error": "Please provide search query"}, status=400)

    medicines = Medicine.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )

    data = []

    for med in medicines:
        inventories = StoreInventory.objects.filter(
            medicine=med,
            stock__gt=0
        ).select_related('store')

        stores = [
            {
                "store_id": inv.store.id,
                "store_name": inv.store.store_name,
                "price": inv.price,
                "stock": inv.stock
            }
            for inv in inventories
        ]

        data.append({
            "medicine_id": med.id,
            "medicine": med.name,
            "requires_prescription": med.requires_prescription,
            "available_stores": stores
        })

    return Response(data)


# 🏪 GET STORES API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stores(request):
    stores = MedicalStore.objects.all()
    serializer = MedicalStoreSerializer(stores, many=True)
    return Response(serializer.data)


# 📦 GET ORDERS API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user

    # ✅ seller view
    if hasattr(user, 'medical_store'):
        orders = Order.objects.filter(store__user=user)
    else:
        # ✅ customer view
        orders = Order.objects.filter(user=user)

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# ✅ CONFIRM ORDER
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        # only store owner can confirm
        if order.store.user != request.user:
            return Response({"error": "Not allowed"}, status=403)

        order.status = "confirmed"
        order.save()

        return Response({"message": "Order confirmed"})

    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)


# ⏰ GET REMINDERS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reminders(request):
    reminders = Reminder.objects.filter(user=request.user)
    serializer = ReminderSerializer(reminders, many=True)
    return Response(serializer.data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order
from reminders.models import Reminder


# 🏪 GET STORES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stores(request):
    stores = MedicalStore.objects.all()

    data = [
        {
            "id": store.id,
            "store_name": store.store_name,
            "address": store.address
        }
        for store in stores
    ]

    return Response(data)


# 🛒 GET ORDERS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user

    if user.role == "seller":
        orders = Order.objects.filter(store__user=user)
    else:
        orders = Order.objects.filter(patient=user)

    data = [
        {
            "id": order.id,
            "store": order.store.store_name,
            "medicine": order.medicine.name,
            "quantity": order.quantity,
            "status": order.status,
            "created_at": order.created_at
        }
        for order in orders
    ]

    return Response(data)


# ⏰ GET REMINDERS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reminders(request):
    reminders = Reminder.objects.filter(user=request.user)

    data = [
        {
            "id": r.id,
            "medicine": r.medicine.name,
            "time": r.reminder_time,
            "frequency_per_day": r.frequency_per_day,
            "start_date": r.start_date,
            "end_date": r.end_date
        }
        for r in reminders
    ]

    return Response(data)

