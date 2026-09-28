from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AccountDeletionRequest
from .serializers import UserSerializer
from .services import get_or_create_firebase_user, issue_tokens, verify_id_token

User = get_user_model()


class FirebaseAuthView(APIView):
    ''' Проверка id_token, создание пользователя в бд, выдача доступа'''
    permission_classes = (AllowAny, )

    @extend_schema(
        request=inline_serializer(
            name='FirebaseAuth',
            fields={
                'id_token': serializers.CharField(),
            }
        ),
        responses={200: inline_serializer(
            name='FirebaseAuth',
            fields={'status': serializers.CharField()}
        )}
    )
    def post(self, request):
        # Проверка и получение данных от пользователя
        data = verify_id_token(id_token=request.data['id_token'])

        # Создание пользователя
        user, created = get_or_create_firebase_user(firebase_uid=data.get('uid'), email=data.get('email'))

        # Выдача доступа пользователю
        tokens = issue_tokens(user)

        return Response({**tokens, 'is_new_user': created})


class MeView(generics.RetrieveUpdateAPIView):
    ''' Получение личных данных пользователем '''
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user
    

class RequestDeletionView(APIView):
    ''' Добавление пользователя в очередь для удаления '''
    permission_classes = (IsAuthenticated, )

    @extend_schema(
        request=inline_serializer(
            name='DeleteUser',
            fields={
                'id_token': serializers.CharField(),
                'reason': serializers.CharField(),
            }
        ),
        responses={200: inline_serializer(
            name='DeleteUser',
            fields={'status': serializers.CharField()}
        )}
    )
    def post(self, request):
        # Проверка данных, токена
        decoded = verify_id_token(id_token=request.data['id_token'])
        #
        if decoded["uid"] != request.user.firebase_uid:
            raise PermissionDenied('Firebase token does not belong to the authenticated user.')
            
        # Отправление запроса на удаление
        req = AccountDeletionRequest.schedule(request.user, reason=request.data.get('reason', ''))
        return Response({'detail': f'Аккаунт будет удалён {req.delete_at:%d.%m.%Y}'})


class CancleDeleteView(APIView):
    ''' Эндпоинт для отмены удаления аккаунта пользователем '''
    permission_classes = (AllowAny, )

    @extend_schema(
        request=inline_serializer(
            name='CancelDeleteUser',
            fields={
                'reason': serializers.CharField(),
            }
        ),
        responses={200: inline_serializer(
            name='CancelDeleteUser',
            fields={'status': serializers.CharField()}
        )}
    )
    def post(self, request):
        # Проверка данных, токена
        verify_id_token(id_token=request.data['id_token'])

        # Отправление запроса на отмену
        req = AccountDeletionRequest.cancel(...)
        return Response({'detail': f'Аккаунт будет удалён {req.delete_at:%d.%m.%Y}'})
        
        