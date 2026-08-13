from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from common.exceptions import api_response

from .models import Address, Order
from .serializers import AddressSerializer, CreateOrderSerializer, OrderSerializer


class AddressViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer
    pagination_class = None

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class OrderViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ("get", "post", "head", "options")

    def get_queryset(self):
        return Order.objects.prefetch_related("items").filter(user=self.request.user)

    def get_serializer_class(self):
        return CreateOrderSerializer if self.action == "create" else OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=("post",), url_path="cancel")
    @transaction.atomic
    def cancel(self, request, pk=None):
        order = get_object_or_404(
            Order.objects.select_for_update().prefetch_related("items"),
            pk=pk,
            user=request.user,
        )
        if order.status != Order.Status.PENDING:
            return api_response(message="只有待支付订单可以取消", code=400)
        for item in order.items.all():
            item.product.__class__.objects.filter(pk=item.product_id).update(stock=F("stock") + item.quantity)
        order.status = Order.Status.CANCELLED
        order.save(update_fields=("status", "updated_at"))
        return api_response(OrderSerializer(order).data, "订单已取消")

    @action(detail=True, methods=("post",), url_path="mock-pay")
    @transaction.atomic
    def mock_pay(self, request, pk=None):
        order = get_object_or_404(Order.objects.select_for_update(), pk=pk, user=request.user)
        if order.status != Order.Status.PENDING:
            return api_response(message="订单状态不可支付", code=400)
        order.status = Order.Status.PAID
        order.paid_at = timezone.now()
        order.save(update_fields=("status", "paid_at", "updated_at"))
        for item in order.items.all():
            item.product.__class__.objects.filter(pk=item.product_id).update(sales=F("sales") + item.quantity)
        return api_response(OrderSerializer(order).data, "模拟支付成功")
