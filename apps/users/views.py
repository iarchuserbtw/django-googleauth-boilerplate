from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics

from .models import User
from .serializers import UserSerializer

    
@method_decorator(csrf_exempt, name='dispatch')
class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('google_token')
        if not token:
            return Response({'error': 'Токен обязателен'}, status=400)

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                'google id'  # вставишь позже
            )
        except ValueError:
            return Response({'error': 'Невалидный токен'}, status=400)

        google_id = idinfo['sub']
        email = idinfo.get('email', '')

        user, created = User.objects.get_or_create(google_id=google_id)
        if created:
            user.email = email
            user.save()

        tokens = get_tokens(user, google_id) # что это

        return Response({
            'tokens': tokens,
        })


class GoogleAuthGenericsView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )
