from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .serializers import UserReadSerializer, UserUpdateSerializer, FirebaseAuthSerializer
from .services import get_or_create_firebase_user, issue_tokens


User = get_user_model()


# class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin):

#     queryset = User.objects.all()
#     permission_classes = (IsAuthenticated, )

#     def get_serializer_class(self):
#         if self.action == 'me_partial':
#             return UserUpdateSerializer
#         return UserReadSerializer

#     @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
#     def me(self, request):
#         """GET /users/me/ — вернуть свой профиль."""
#         serializer = self.get_serializer(request.user)
#         return Response(serializer.data)

#     @me.mapping.patch  # ← PATCH /users/me/ уходит сюда, а не в me()
#     def me_partial(self, request):
#         """PATCH /users/me/ — частично обновить свой профиль."""
#         serializer = self.get_serializer(
#             request.user, data=request.data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# users/views.py
class FirebaseAuthView(APIView):
    """POST /api/auth/firebase/ — единственная дверь регистрации/входа."""
    permission_classes = [AllowAny]

    # Документация api
    @extend_schema(
        tags=['Auth'],
        summary='Аутентификация через Firebase',
        request=FirebaseAuthSerializer,
        # responses={200: FirebaseLoginResponseSerializer, 201: FirebaseLoginResponseSerializer},
        auth=[],
    )
    def post(self, request):
        # Проверка данных, токена
        serializer = FirebaseAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Данные пользователя
        data = serializer.validated_data

        # Создание пользователя
        user, created = get_or_create_firebase_user(firebase_uid=data['firebase_uid'], email=data['email'])
        
        tokens = issue_tokens(user)

        # HTTP
        return Response({**tokens, 'is_new_user': created})


# аутентификацию пользователя сделать отдельно, для изменения данных сделать отедельные эндпоинты