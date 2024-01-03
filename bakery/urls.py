from rest_framework_nested import routers

from .views import (
    ProductViewSet,
    CategoryViewSet,
    CartViewSet,
    CartItemViewSet,
    OrderViewSet,
)

app_name = 'bakery'

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'order', OrderViewSet, basename='order')

cart_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart_items_detail')
urlpatterns = router.urls + cart_router.urls
