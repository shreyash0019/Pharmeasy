from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer
from .models import User


# ✅ REGISTER
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# ✅ CUSTOM LOGIN (IMPORTANT FIX)
class CustomLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        # get tokens from default JWT view
        response = super().post(request, *args, **kwargs)

        # ✅ add user data in response
        response.data['user'] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        return response
