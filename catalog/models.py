from django.db import models


class Category(models.Model):
    name = models.CharField("名称", max_length=50, unique=True)
    sort_order = models.PositiveIntegerField("排序", default=0)
    is_active = models.BooleanField("启用", default=True)

    class Meta:
        db_table = "catalog_category"
        ordering = ("sort_order", "id")
        verbose_name = "商品分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField("名称", max_length=120, db_index=True)
    description = models.TextField("描述", blank=True)
    image_url = models.URLField("图片地址", max_length=500, blank=True)
    price = models.DecimalField("价格", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("库存", default=0)
    sales = models.PositiveIntegerField("销量", default=0)
    is_active = models.BooleanField("上架", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "catalog_product"
        ordering = ("-id",)
        indexes = [models.Index(fields=("category", "is_active"), name="product_category_active")]
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

