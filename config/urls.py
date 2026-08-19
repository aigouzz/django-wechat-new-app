from django.contrib import admin
from django.urls import include, path
from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/", include("common.urls")),
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/catalog/", include("catalog.urls")),
    path("api/v1/cart/", include("cart.urls")),
    path("api/v1/orders/", include("orders.urls")),
]

