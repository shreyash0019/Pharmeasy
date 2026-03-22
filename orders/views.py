from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer
from pharmacy.utils import send_fcm_notification

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # 🔹 required for router
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "seller":
            return Order.objects.filter(store__user=user).order_by('-created_at')
        return Order.objects.filter(patient=user).order_by('-created_at')

    def perform_create(self, serializer):
        order = serializer.save(patient=self.request.user)
        store_user = order.store.user
        if store_user.fcm_token:
            send_fcm_notification(
                store_user.fcm_token,
                "New Order",
                f"New order for {order.medicine.name}"
            )

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.store.user != request.user:
            return Response({"error": "Not allowed"}, status=403)

        order.status = 'confirmed'
        order.save()

        patient = order.patient
        if patient.fcm_token:
            send_fcm_notification(
                patient.fcm_token,
                "Order Confirmed",
                f"Your order for {order.medicine.name} is confirmed"
            )

        return Response({"message": "Order Confirmed"})
