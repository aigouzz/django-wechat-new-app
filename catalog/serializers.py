from rest_framework import serializers

from .models import Category, Product, JDProduct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = ("id", "category", "category_name", "name", "description", "image_url", "price", "stock", "sales")

class GetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = JDProduct
        fields = ["skuId", "skuName", "priceInfo"]

