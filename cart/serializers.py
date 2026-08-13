from rest_framework import serializers

from catalog.models import Product
from catalog.serializers import ProductSerializer

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source="product", queryset=Product.objects.filter(is_active=True), write_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id", "product", "product_id", "quantity", "selected", "subtotal")

    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity

    def validate(self, attrs):
        product = attrs.get("product") or getattr(self.instance, "product", None)
        quantity = attrs.get("quantity", getattr(self.instance, "quantity", 1))
        if quantity < 1:
            raise serializers.ValidationError("数量必须大于0")
        if product and quantity > product.stock:
            raise serializers.ValidationError("商品库存不足")
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        item, created = CartItem.objects.get_or_create(user=user, product=validated_data["product"], defaults=validated_data)
        if not created:
            item.quantity += validated_data.get("quantity", 1)
            self.instance = item
            self.validate({"quantity": item.quantity})
            item.save(update_fields=("quantity",))
        return item

