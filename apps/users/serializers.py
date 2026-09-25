import re

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'display_name', 'email', 'updated_at', )
        read_only_fields = ('email', 'updated_at', )

    def validate_username(self, value):
        if not re.fullmatch(r'[a-z0-9_]{3,30}', value):
            raise serializers.ValidationError(
                '3-30 символов: латиница, цифры, подчёркивание'
            )
        return value.lower()

    def validate_display_name(self, value):
        if not re.fullmatch(r'[a-z0-9_]{3,25}', value):
            raise serializers.ValidationError(
                '3-25 символов: латиница, цифры, подчёркивание'
            )
        return value.lower()
