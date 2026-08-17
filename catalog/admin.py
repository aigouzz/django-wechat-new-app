from django.contrib import admin

from .models import Category, Product, JDProduct, Course


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock", "sales", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    list_select_related = ("category",)

@admin.register(JDProduct)
class JDProductAdmin(admin.ModelAdmin):
    list_display = ("skuId", "skuName", "priceInfo", "shopInfo", "cid1", 'cid2', 'cid3', 'price', 'commissionInfo')
    search_fields = ("skuName",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "teacher", "price", 'detail', 'created_at')
    search_fields = ("name",)

