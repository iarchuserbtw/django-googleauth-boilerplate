from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import (
    CancelDeletionView,
    FirebaseAuthView,
    MeView,
    RequestDeletionView,
)

urlpatterns = [
    path("api/auth/firebase/", FirebaseAuthView.as_view(), name="firebase-auth"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/me/", MeView.as_view(), name="me_view"),
    path("api/users/me/deletion/", RequestDeletionView.as_view(), name="delete_user"),
    path(
        "api/users/me/deletion/cancel/",
        CancelDeletionView.as_view(),
        name="cancel_delete_user",
    ),
]
