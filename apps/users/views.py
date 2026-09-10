from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserCreateSerializer, UserReadSerializer, UserUpdateSerializer

User = get_user_model()


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()  # ← обязательно для GenericViewSet

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'me_partial':
            return UserUpdateSerializer
        return UserReadSerializer  # дефолт — для чтения

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """GET /users/me/ — вернуть свой профиль."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @me.mapping.patch  # ← PATCH /users/me/ уходит сюда, а не в me()
    def me_partial(self, request):
        """PATCH /users/me/ — частично обновить свой профиль."""
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)