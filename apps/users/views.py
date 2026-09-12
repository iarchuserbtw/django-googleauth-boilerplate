from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserCreateSerializer, UserReadSerializer, UserUpdateSerializer, FirebaseAuthSerializer
from .services import get_or_create_firebase_user, issue_tokens


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


# users/views.py
class FirebaseAuthView(APIView):
    """POST /api/auth/firebase/ — единственная дверь регистрации/входа."""
    permission_classes = [AllowAny]

    def post(self, request):
        # шаги 1–3: проверка и распаковка (или 400)
        serializer = FirebaseAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        # шаги 4–5: бизнес-логика
        user, created = get_or_create_firebase_user(
            firebase_uid=data['firebase_uid'],
            email=data['email'],
            display_name=data['display_name'],
        )
        tokens = issue_tokens(user)

        # шаг 6: HTTP
        return Response({**tokens, 'is_new_user': created})