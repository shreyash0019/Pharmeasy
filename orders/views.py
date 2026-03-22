from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer

# 🔔 FCM
from pharmacy.utils import send_fcm_notification


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # 🔹 add this
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    # 🔥 FILTER DATA BASED ON USER ROLE
    def get_queryset(self):
        user = self.request.user

        # 🏪 Seller
        if user.role == "seller":
            return Order.objects.filter(store__user=user).order_by('-created_at')

        # 👤 Patient
        return Order.objects.filter(patient=user).order_by('-created_at')

    # 🔥 AUTO SET PATIENT + SEND NOTIFICATION
    def perform_create(self, serializer):
        order = serializer.save(patient=self.request.user)

        # 🔔 Notify seller
        store_user = order.store.user
        if store_user.fcm_token:
            send_fcm_notification(
                store_user.fcm_token,
                "New Order",
                f"New order for {order.medicine.name}"
            )

    # 🔥 CONFIRM ORDER (ONLY SELLER)
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()

        # ❌ prevent unauthorized users
        if order.store.user != request.user:
            return Response({"error": "Not allowed"}, status=403)

        order.status = 'confirmed'
        order.save()

        # 🔔 Notify patient
        patient = order.patient
        if patient.fcm_token:
            send_fcm_notification(
                patient.fcm_token,
                "Order Confirmed",
                f"Your order for {order.medicine.name} is confirmed"
            )

        return Response({"message": "Order Confirmed"})
