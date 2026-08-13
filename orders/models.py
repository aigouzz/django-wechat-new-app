from django.conf import settings
from django.db import models

from catalog.models import Product


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    recipient = models.CharField("收件人", max_length=50)
    mobile = models.CharField("手机号", max_length=20)
    province = models.CharField("省", max_length=50)
    city = models.CharField("市", max_length=50)
    district = models.CharField("区县", max_length=50)
    detail = models.CharField("详细地址", max_length=200)
    is_default = models.BooleanField("默认地址", default=False)

    class Meta:
        db_table = "orders_address"
        ordering = ("-is_default", "-id")


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "待支付"
        PAID = "paid", "已支付"
        SHIPPED = "shipped", "已发货"
        COMPLETED = "completed", "已完成"
        CANCELLED = "cancelled", "已取消"

    order_no = models.CharField("订单号", max_length=32, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField("状态", max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    total_amount = models.DecimalField("总金额", max_digits=12, decimal_places=2)
    recipient = models.CharField("收件人", max_length=50)
    mobile = models.CharField("手机号", max_length=20)
    full_address = models.CharField("收货地址", max_length=300)
    remark = models.CharField("备注", max_length=200, blank=True)
    paid_at = models.DateTimeField("支付时间", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "orders_order"
        ordering = ("-id",)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField("商品名称", max_length=120)
    image_url = models.URLField("商品图片", max_length=500, blank=True)
    price = models.DecimalField("成交单价", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("数量")

    class Meta:
        db_table = "orders_order_item"

