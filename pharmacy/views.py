from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Medicine, StoreInventory, MedicalStore, Reminder
from orders.models import Order
from .serializers import MedicineSerializer, StoreInventorySerializer, MedicalStoreSerializer, OrderSerializer, ReminderSerializer

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
    queryset = StoreInventory.objects.select_related('store','medicine')
    serializer_class = StoreInventorySerializer
    permission_classes = [IsAuthenticated]

# 🔍 Search Medicines (ALL users see results)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_medicine(request):
    q = request.GET.get('q','').strip()
    if not q:
        return Response([])
    items = StoreInventory.objects.select_related('medicine','store').filter(
        medicine__name__icontains=q,
        stock__gt=0
    ).order_by('price')
    result = []
    for i in items:
        result.append({
            "medicine": i.medicine.name,
            "store": i.store.store_name,
            "price": i.price,
            "stock": i.stock
        })
    return Response(result)

# 🏪 Get all stores
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stores(request):
    stores = MedicalStore.objects.all()
    return Response(MedicalStoreSerializer(stores, many=True).data)

# ⏰ Get reminders (ALL users see all)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reminders(request):
    reminders = Reminder.objects.all()
    return Response(ReminderSerializer(reminders, many=True).data)

# ⏰ Create reminder (ALL users)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reminder(request):
    serializer = ReminderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# 🛒 Get orders (ALL users see all)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.all()
    return Response(OrderSerializer(orders, many=True).data)

# 🛒 Create order (ALL users)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
