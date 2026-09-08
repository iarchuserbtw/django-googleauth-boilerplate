from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'display_name', 'phone', 'email', 'google_id',
            'created_at', 'updated_at',
            'last_activity', 
            'is_active', 'is_staff'
        )
        read_only_fields = ('created_at', 'updated_at', 'last_activity', 'is_active', 'is_staff')

    def create(self, validated_data):
        print(validated_data)
        return User.objects.create(**validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'username', 'display_name', 'phone'
        