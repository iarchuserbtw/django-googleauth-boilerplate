from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'display_name', 'phone', 'email', 'google_id',
            'created_at', 'updated_at',
            'last_activity', 
            'is_active', 'is_staff'
        )
        read_only_fields = ('created_at', 'updated_at', 'last_activity', 'google_id', 'email')

    def create(self, validated_data):
        google_id = validated_data.get('google_id')
        print(google_id)
        return User.objects.create(**validated_data)