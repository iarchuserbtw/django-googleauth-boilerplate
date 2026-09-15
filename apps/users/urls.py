from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from apps.users.views import FirebaseAuthView, MeView, RequestDeletionView

urlpatterns = [
    path('api/auth/', FirebaseAuthView.as_view(), name='firebase-auth'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/user/', MeView.as_view(), name='me_view'),
    path('api/user/', RequestDeletionView.as_view(), name='me_view'),
]