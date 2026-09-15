from django.contrib.auth import get_user_model
from django.views import generic
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AccountDeletionRequest
from .serializers import FirebaseAuthSerializer, UserSerializer
from .services import get_or_create_firebase_user, issue_tokens

User = get_user_model()


class FirebaseAuthView(APIView):
    """POST /api/auth/firebase/ — единственная дверь регистрации/входа."""
    permission_classes = [AllowAny]

    # Документация api
    @extend_schema(
        tags=['auth'],
        request=FirebaseAuthSerializer,
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


class MeView(generics.RetrieveUpdateAPIView):
    ''' Получение личных данных пользователем '''
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user
    

class RequestDeletionView(APIView):
    ''' Добавление пользователя в ожидание для удаления '''
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        # Проверка данных, токена
        serializer = FirebaseAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Отправление запроса на удаление
        req = AccountDeletionRequest.schedule(request.user, reason=request.data.get('reason', ''))
        return Response({'detail': f'Аккаунт будет удалён {req.delete_at:%d.%m.%Y}'})


class CancleDeleteView(APIView):
    ''' Эндпоинт для отмены удаления аккаунта пользователем '''
    permission_classes = (AllowAny, )

    def post(self, request):
        # Проверка данных, токена
        serializer = FirebaseAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Отправление запроса на отмену
        req = AccountDeletionRequest.cancel(...)
        return Response({'detail': f'Аккаунт будет удалён {req.delete_at:%d.%m.%Y}'})
        
        