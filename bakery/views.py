from rest_framework import viewsets, parsers, permissions

from authentication.models import User
from .models import ProductModel, CategoryModel, CartModel, CartItemModel, OrderModel
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer, \
    AddCartItemSerializer, UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (parsers.MultiPartParser,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = CartModel.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItemModel.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OrderModel.objects.all()
        customer_id = User.objects.only('id').get(id=user.id)
        return OrderModel.objects.filter(customer_id=customer_id)
