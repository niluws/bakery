from rest_framework import serializers

from .models import ProductModel, CategoryModel


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'
