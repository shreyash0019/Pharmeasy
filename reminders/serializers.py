from rest_framework import serializers
from .models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    # 🔹 readable user name
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Reminder
        fields = [
            'id',
            'user',
            'user_name',
            'message',
            'remind_at'
        ]

        read_only_fields = ['user']

    # 🔥 auto assign logged-in user
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
