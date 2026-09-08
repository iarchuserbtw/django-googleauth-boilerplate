from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)

from apps.users.views import GoogleAuthView, MeView, GoogleTestView, GoogleAuthGenericsView



urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/google/', GoogleAuthView.as_view(), name='google-authentication'),
    path('auth/me/', MeView.as_view(), name='me'),

    path('auth/test/', GoogleTestView.as_view()),
    path('auth/generic_test/', GoogleAuthGenericsView.as_view())
]