from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.users.views import FirebaseAuthView

from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    # path('api/auth/', include(router.urls)),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/firebase/', FirebaseAuthView.as_view(), name='firebase-auth'),
    
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]