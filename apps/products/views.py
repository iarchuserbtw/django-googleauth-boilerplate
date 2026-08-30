from rest_framework import generics, viewsets

from .models import Product, ProductImage
from .serializers import ProductSerializer


class ProductListCreateViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    