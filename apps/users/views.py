from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics

from .models import User
from .serializers import UserCreateSerializer, UserUpdateSerializer


class GoogleAuthGenericsView(generics.CreateAPIView):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserUpdateSerializer

    permission_classes = (AllowAny, )
