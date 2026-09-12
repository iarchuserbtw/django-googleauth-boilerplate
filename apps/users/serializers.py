from rest_framework import serializers

from .models import User

import re


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('display_name', 'email', 'firebase_uid')

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


# users/serializers.py
from rest_framework import serializers
from firebase_admin import auth as fb_auth


class FirebaseAuthSerializer(serializers.Serializer):
    """Принимает id_token от Firebase (любой провайдер входа:
    google, email+пароль) и валидирует его."""

    id_token = serializers.CharField(write_only=True)

    # Заполнятся в validate() после проверки — клиент их не присылает
    firebase_uid = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    display_name = serializers.CharField(read_only=True, allow_blank=True)

    def validate(self, attrs):
        try:
            decoded = fb_auth.verify_id_token(attrs['id_token'])
        except fb_auth.InvalidIdTokenError:
            raise serializers.ValidationError(
                {'id_token': 'Токен невалиден или истёк'})
        except fb_auth.RevokedIdTokenError:
            raise serializers.ValidationError(
                {'id_token': 'Токен отозван'})
        except Exception:
            raise serializers.ValidationError(
                {'id_token': 'Не удалось проверить токен'})

        attrs['firebase_uid'] = decoded['uid']
        attrs['email'] = decoded.get('email', '')
        attrs['display_name'] = decoded.get('name', '')
        return attrs
