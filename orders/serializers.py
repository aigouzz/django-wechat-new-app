import uuid
from decimal import Decimal

from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from cart.models import CartItem
from catalog.models import Product

from .models import Address, Order, OrderItem


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ("user",)

    def create(self, validated_data):
        user = self.context["request"].user
        if validated_data.get("is_default"):
            user.addresses.update(is_default=False)
        return Address.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("is_default"):
            instance.user.addresses.exclude(pk=instance.pk).update(is_default=False)
        return super().update(instance, validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_name", "image_url", "price", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = ("id", "order_no", "status", "status_display", "total_amount", "recipient", "mobile", "full_address", "remark", "paid_at", "created_at", "items")


class CreateOrderSerializer(serializers.Serializer):
    address_id = serializers.PrimaryKeyRelatedField(source="address", queryset=Address.objects.none())
    cart_item_ids = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=False)
    remark = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["address_id"].queryset = Address.objects.filter(user=request.user)

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        cart_items = list(
            CartItem.objects.select_related("product")
            .filter(user=user, id__in=validated_data["cart_item_ids"])
            .order_by("id")
        )
        if len(cart_items) != len(set(validated_data["cart_item_ids"])):
            raise serializers.ValidationError("购物车商品不存在")

        product_ids = [item.product_id for item in cart_items]
        locked_products = {
            product.id: product
            for product in Product.objects.select_for_update().filter(id__in=product_ids, is_active=True)
        }
        total = Decimal("0.00")
        for item in cart_items:
            product = locked_products.get(item.product_id)
            if not product or item.quantity > product.stock:
                raise serializers.ValidationError(f"{item.product.name}库存不足或已下架")
            total += product.price * item.quantity

        address = validated_data["address"]
        order = Order.objects.create(
            order_no=uuid.uuid4().hex.upper(),
            user=user,
            total_amount=total,
            recipient=address.recipient,
            mobile=address.mobile,
            full_address=f"{address.province}{address.city}{address.district}{address.detail}",
            remark=validated_data.get("remark", ""),
        )
        order_items = []
        for item in cart_items:
            product = locked_products[item.product_id]
            order_items.append(OrderItem(order=order, product=product, product_name=product.name, image_url=product.image_url, price=product.price, quantity=item.quantity))
            Product.objects.filter(pk=product.pk).update(stock=F("stock") - item.quantity)
        OrderItem.objects.bulk_create(order_items)
        CartItem.objects.filter(user=user, id__in=validated_data["cart_item_ids"]).delete()
        return order

