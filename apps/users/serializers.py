from rest_framework import serializers

from firebase_admin import auth as fb_auth

import re

from .models import User


class FirebaseAuthSerializer(serializers.Serializer):
    """Принимает id_token от Firebase (любой провайдер входа:
    google, email+пароль) и валидирует его."""

    id_token = serializers.CharField(write_only=True)
    # read only поля email firbaseuid убраны, потому что они не должны передаваться пользователяи

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
        fields = ('username', 'email', 'display_name', 'phone', 'created_at', 'updated_at', 'last_activity', )




class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('display_name', 'email', 'firebase_uid')
