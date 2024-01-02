from django.urls import path

from .views import (
    ProductListAPI,
)

app_name = 'bakery'

urlpatterns = [
    path('product_list/', ProductListAPI.as_view(), name='product_list'),
]
