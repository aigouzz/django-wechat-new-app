from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("catalog", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("recipient", models.CharField(max_length=50, verbose_name="收件人")),
                ("mobile", models.CharField(max_length=20, verbose_name="手机号")),
                ("province", models.CharField(max_length=50, verbose_name="省")),
                ("city", models.CharField(max_length=50, verbose_name="市")),
                ("district", models.CharField(max_length=50, verbose_name="区县")),
                ("detail", models.CharField(max_length=200, verbose_name="详细地址")),
                ("is_default", models.BooleanField(default=False, verbose_name="默认地址")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="addresses", to=settings.AUTH_USER_MODEL)),
            ],
            options={"db_table": "orders_address", "ordering": ("-is_default", "-id")},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order_no", models.CharField(max_length=32, unique=True, verbose_name="订单号")),
                ("status", models.CharField(choices=[("pending", "待支付"), ("paid", "已支付"), ("shipped", "已发货"), ("completed", "已完成"), ("cancelled", "已取消")], db_index=True, default="pending", max_length=20, verbose_name="状态")),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="总金额")),
                ("recipient", models.CharField(max_length=50, verbose_name="收件人")),
                ("mobile", models.CharField(max_length=20, verbose_name="手机号")),
                ("full_address", models.CharField(max_length=300, verbose_name="收货地址")),
                ("remark", models.CharField(blank=True, max_length=200, verbose_name="备注")),
                ("paid_at", models.DateTimeField(blank=True, null=True, verbose_name="支付时间")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orders", to=settings.AUTH_USER_MODEL)),
            ],
            options={"db_table": "orders_order", "ordering": ("-id",)},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_name", models.CharField(max_length=120, verbose_name="商品名称")),
                ("image_url", models.URLField(blank=True, max_length=500, verbose_name="商品图片")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="成交单价")),
                ("quantity", models.PositiveIntegerField(verbose_name="数量")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="orders.order")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="catalog.product")),
            ],
            options={"db_table": "orders_order_item"},
        ),
    ]

