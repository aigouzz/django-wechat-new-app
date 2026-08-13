from django.contrib import admin

from .models import Address, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "price", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_no", "user", "status", "total_amount", "recipient", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("order_no", "recipient", "mobile", "user__username")
    list_select_related = ("user",)
    inlines = (OrderItemInline,)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipient", "mobile", "city", "is_default")

