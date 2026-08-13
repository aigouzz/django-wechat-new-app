from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="名称")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="排序")),
                ("is_active", models.BooleanField(default=True, verbose_name="启用")),
            ],
            options={"verbose_name": "商品分类", "verbose_name_plural": "商品分类", "db_table": "catalog_category", "ordering": ("sort_order", "id")},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(db_index=True, max_length=120, verbose_name="名称")),
                ("description", models.TextField(blank=True, verbose_name="描述")),
                ("image_url", models.URLField(blank=True, max_length=500, verbose_name="图片地址")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="价格")),
                ("stock", models.PositiveIntegerField(default=0, verbose_name="库存")),
                ("sales", models.PositiveIntegerField(default=0, verbose_name="销量")),
                ("is_active", models.BooleanField(default=True, verbose_name="上架")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="catalog.category")),
            ],
            options={"verbose_name": "商品", "verbose_name_plural": "商品", "db_table": "catalog_product", "ordering": ("-id",), "indexes": [models.Index(fields=["category", "is_active"], name="product_category_active")]},
        ),
    ]

