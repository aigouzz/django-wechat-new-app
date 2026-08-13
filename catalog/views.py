from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    pagination_class = None
    queryset = Category.objects.filter(is_active=True)


class ProductViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    filterset_fields = ("category",)
    search_fields = ("name", "description")
    ordering_fields = ("price", "sales", "created_at")
    queryset = Product.objects.select_related("category").filter(is_active=True)

