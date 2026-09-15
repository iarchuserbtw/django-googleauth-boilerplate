import re

from firebase_admin import auth as fb_auth
from rest_framework import serializers

from .models import User


# Убрать это отсюда
class FirebaseAuthSerializer(serializers.Serializer):
    """Принимает id_token от Firebase (любой провайдер входа:
    google, email+пароль) и валидирует его."""

    id_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            decoded = fb_auth.verify_id_token(attrs['id_token'], check_revoked=True)
        except fb_auth.InvalidIdTokenError:
            raise serializers.ValidationError(
                {'id_token': 'Токен невалиден или истёк'})

        if not decoded.get("email"):
                raise serializers.ValidationError({"id_token": "В токене нет email"})

        attrs['firebase_uid'] = decoded['uid']
        attrs['email'] = decoded.get('email', '')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'display_name', 'email', 'updated_at', )
        read_only_fields = ('email', 'updated_at', )

    def validate_username(self, value):
        if not re.fullmatch(r'[a-z0-9_]{3,15}', value):
            raise serializers.ValidationError(
                '3-15 символов: латиница, цифры, подчёркивание'
            )
        return value.lower()

    def validate_display_name(self, value):
        if not re.fullmatch(r'[a-z0-9_]{3,15}', value):
            raise serializers.ValidationError(
                '3-15 символов: латиница, цифры, подчёркивание'
            )
        return value.lower()

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'display_name', 'phone')

    def validate_username(self, value):
        if not re.fullmatch(r'[a-z0-9_]{3,30}', value):
            raise serializers.ValidationError(
                '3-30 символов: латиница, цифры, подчёркивание'
            )
        return value.lower()