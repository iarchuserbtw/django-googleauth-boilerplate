from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from apps.users.views import (
    CancleDeleteView,
    FirebaseAuthView,
    MeView,
    RequestDeletionView,
)

urlpatterns = [
    path('api/auth/', FirebaseAuthView.as_view(), name='firebase-auth'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/user/', MeView.as_view(), name='me_view'),
    path('api/user/delete/', RequestDeletionView.as_view(), name='delete_user'),
    path('api/user/cancle_delete/', CancleDeleteView.as_view(), name='cancle_delete_user'),
]