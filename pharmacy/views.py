from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Medicine, StoreInventory, MedicalStore
from .serializers import (
    MedicineSerializer,
    StoreInventorySerializer,
    MedicalStoreSerializer
)


# 🔹 MEDICINE CRUD
class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]


# 🔹 MEDICAL STORE CRUD
class MedicalStoreViewSet(viewsets.ModelViewSet):
    queryset = MedicalStore.objects.all()
    serializer_class = MedicalStoreSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 🔹 STORE INVENTORY CRUD
class StoreInventoryViewSet(viewsets.ModelViewSet):
    queryset = StoreInventory.objects.all()
    serializer_class = StoreInventorySerializer
    permission_classes = [IsAuthenticated]


# 🔹 SEARCH MEDICINE
@api_view(['GET'])
def search_medicine(request):
    name = request.GET.get('name')

    if not name:
        return Response({"error": "Please provide medicine name"}, status=400)

    medicines = Medicine.objects.filter(name__icontains=name)

    data = []

    for med in medicines:
        inventories = StoreInventory.objects.filter(
            medicine=med,
            stock__gt=0
        )

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