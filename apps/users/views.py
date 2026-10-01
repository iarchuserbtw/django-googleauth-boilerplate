from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, serializers
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AccountDeletionRequest
from .serializers import UserSerializer
from .services import (
    get_or_create_firebase_user,
    get_user_data_deletion,
    issue_tokens,
    verify_id_token,
)

User = get_user_model()


class FirebaseAuthView(APIView):
    """Проверка id_token, создание пользователя в бд, выдача доступа"""

    permission_classes = (AllowAny,)

    @extend_schema(
        request=inline_serializer(
            name="FirebaseAuth",
            fields={
                "id_token": serializers.CharField(),
            },
        ),
        responses={200: inline_serializer(name="FirebaseAuth", fields={"status": serializers.CharField()})},
    )
    def post(self, request):
        # Проверка и получение данных от пользователя
        data = verify_id_token(id_token=request.data["id_token"])

        # Создание пользователя
        user, created = get_or_create_firebase_user(firebase_uid=data.get("uid"), email=data.get("email"))

        if not user.is_active:
            data = get_user_data_deletion(user=user)
            return Response(
                {
                    "detail": "Account is scheduled for deletion.",
                    "delete_at": data.delete_at,
                }
            )

        # Выдача доступа пользователю
        tokens = issue_tokens(user)

        return Response({**tokens, "is_new_user": created})


class MeView(generics.RetrieveUpdateAPIView):
    """Получение личных данных пользователем"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class RequestDeletionView(APIView):
    """Добавление пользователя в очередь для удаления"""

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=inline_serializer(
            name="DeleteUser",
            fields={
                "id_token": serializers.CharField(),
                "reason": serializers.CharField(),
            },
        ),
        responses={200: inline_serializer(name="DeleteUser", fields={"status": serializers.CharField()})},
    )
    def post(self, request):
        # Проверка данных, токена
        decoded = verify_id_token(id_token=request.data["id_token"])
        # Проверка на то тот ли пользователь хочет удалить аккаунт
        if decoded["uid"] != request.user.firebase_uid:
            raise PermissionDenied("Firebase token does not belong to the authenticated user.")

        # Отправление запроса на удаление
        req = AccountDeletionRequest.schedule(request.user, reason=request.data.get("reason", ""))
        return Response({"detail": f"Аккаунт будет удалён {req.delete_at:%d.%m.%Y}"})


class CancelDeletionView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=inline_serializer(
            name="CancelDeleteUser",
            fields={
                "id_token": serializers.CharField(),
            },
        ),
        responses={200: inline_serializer(name="CancelDeleteUser", fields={"status": serializers.CharField()})},
    )
    def post(self, request):
        decoded = verify_id_token(request.data["id_token"])

        user = User.objects.get(firebase_uid=decoded["uid"])

        if user is None:
            raise ValidationError("User not found")

        deletion_request = AccountDeletionRequest.objects.get(
            user=user,
            is_cancelled=False,
        )

        if deletion_request is None:
            raise ValidationError("No active account deletion request found.")

        deletion_request.cancel()

        return Response({"detail": "Аккаунт восстановлен"})
