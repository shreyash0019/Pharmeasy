from rest_framework import serializers
from .models import Reminder

class ReminderSerializer(serializers.ModelSerializer):
    # 🔹 Readable fields for frontend
    user_name = serializers.CharField(source='user.username', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = Reminder
        fields = [
            'id',
            'user',
            'user_name',
            'medicine',
            'medicine_name',
            'reminder_time',
            'frequency_per_day',
            'start_date',
            'end_date',
            'created_at'
        ]
        read_only_fields = ['user', 'created_at']

    # 🔥 Auto-assign logged-in user
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
