from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    # 🔥 FILTER DATA BASED ON USER TYPE
    def get_queryset(self):
        user = self.request.user

        # 🏪 Seller (has medical store)
        if hasattr(user, 'medical_store'):
            return Order.objects.filter(store__user=user)

        # 👤 Patient
        return Order.objects.filter(patient=user)

    # 🔥 AUTO SET PATIENT
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

    # 🔥 CONFIRM ORDER (ONLY SELLER CAN DO)
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()

        # ❌ prevent unauthorized users
        if order.store.user != request.user:
            return Response({"error": "Not allowed"}, status=403)

        order.status = 'confirmed'
        order.save()

        return Response({"message": "Order Confirmed"})
