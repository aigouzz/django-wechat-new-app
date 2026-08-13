from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "nickname", "mobile", "is_staff", "date_joined", "updated_at", "is_disabled")
    search_fields = ("username", "nickname", "mobile", "openid")
    fieldsets = UserAdmin.fieldsets + (
        ("微信信息", {"fields": ("openid", "nickname", "avatar_url", "mobile")}),
    )

