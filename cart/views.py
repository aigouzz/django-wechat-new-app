from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import CartItem
from .serializers import CartItemSerializer


class CartItemViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartItemSerializer
    pagination_class = None
    http_method_names = ("get", "post", "patch", "delete", "head", "options")

    def get_queryset(self):
        return CartItem.objects.select_related("product", "product__category").filter(user=self.request.user)

