from django.urls import path, include

from rest_framework import routers, urlpatterns

from .views import ProductListCreateViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductListCreateViewSet)

urlpatterns = [
    path('', include(router.urls))
]

