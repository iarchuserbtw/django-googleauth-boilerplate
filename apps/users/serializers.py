from rest_framework import serializers

from .models import User

import re

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'display_name', 'email', 'firebase_uid',
            'created_at', 'updated_at',
            'last_activity', 
            'is_active', 'is_staff'
        )
        read_only_fields = ('created_at', 'updated_at', 'last_activity', 'is_active', 'is_staff')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'display_name', 'phone')

    def validate_username(self, value):
        # ModelForm-уникальность DRF проверит сам, а формат — здесь:
        if not re.fullmatch(r'[a-z0-9_]{3,30}', value):
            raise serializers.ValidationError(
                '3-30 символов: латиница, цифры, подчёркивание'
            )
        return value.lower()

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'display_name', 'phone')

