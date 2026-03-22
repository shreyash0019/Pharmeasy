from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def validate_password(self, value):
        # ✅ Validate password strength
        validate_password(value)
        return value

    @transaction.atomic
    def create(self, validated_data):
        # Use create_user to handle hashing
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user
