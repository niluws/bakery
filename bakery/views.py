from rest_framework import generics

from .models import ProductModel
from .serializers import ProductSerializer


class ProductListAPI(generics.ListCreateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
