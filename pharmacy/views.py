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

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'medical_store'):
            return MedicalStore.objects.filter(user=user)
        return MedicalStore.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 📦 INVENTORY
class StoreInventoryViewSet(viewsets.ModelViewSet):
    queryset = StoreInventory.objects.all()
    serializer_class = StoreInventorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'medical_store'):
            return StoreInventory.objects.filter(store__user=user)
        return StoreInventory.objects.all()


# 🔍 SEARCH
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
                "store_id": i.store.id,
                "store_name": i.store.store_name,
                "price": i.price,
                "stock": i.stock
            }
            for i in inventories
        ]

        data.append({
            "medicine_id": med.id,
            "medicine": med.name,
            "description": med.description,
            "requires_prescription": med.requires_prescription,
            "available_stores": stores
        })

    return Response(data)


# 🛒 GET ORDERS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user

    # ⚠️ SAFE role check (avoids crash if role not present)
    if hasattr(user, 'role') and user.role == "seller":
        orders = Order.objects.filter(store__user=user)
    else:
        orders = Order.objects.filter(patient=user)

    return Response(OrderSerializer(orders, many=True).data)


# 🏪 GET STORES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stores(request):
    stores = MedicalStore.objects.all()
    serializer = MedicalStoreSerializer(stores, many=True)
    return Response(serializer.data)


# ⏰ GET REMINDERS (ADD THIS — missing earlier ❗)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reminders(request):
    reminders = Reminder.objects.filter(user=request.user)
    return Response(ReminderSerializer(reminders, many=True).data)
