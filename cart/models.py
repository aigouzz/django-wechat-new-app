from django.conf import settings
from django.db import models

from catalog.models import Product


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("数量", default=1)
    selected = models.BooleanField("选中", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "cart_item"
        constraints = [models.UniqueConstraint(fields=("user", "product"), name="unique_user_product_cart")]
        ordering = ("-id",)

