from rest_framework.test import APITestCase

from catalog.models import Category, Product
from orders.models import Address, Order


class ShopFlowTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="测试分类")
        self.product = Product.objects.create(category=category, name="测试商品", price="10.00", stock=10)

    def login(self):
        response = self.client.post("/api/v1/auth/wechat-login/", {"code": "test-code"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['data']['access']}")

    def test_complete_order_flow(self):
        self.login()
        cart = self.client.post("/api/v1/cart/items/", {"product_id": self.product.id, "quantity": 2}, format="json")
        self.assertEqual(cart.status_code, 201)
        address = self.client.post(
            "/api/v1/orders/addresses/",
            {"recipient": "张三", "mobile": "13800000000", "province": "广东省", "city": "深圳市", "district": "南山区", "detail": "科技园1号", "is_default": True},
            format="json",
        )
        self.assertEqual(address.status_code, 201)
        order = self.client.post(
            "/api/v1/orders/orders/",
            {"address_id": address.data["id"], "cart_item_ids": [cart.data["id"]]},
            format="json",
        )
        self.assertEqual(order.status_code, 201)
        self.assertEqual(order.data["status"], Order.Status.PENDING)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)
        paid = self.client.post(f"/api/v1/orders/orders/{order.data['id']}/mock-pay/")
        self.assertEqual(paid.status_code, 200)
        self.assertEqual(paid.data["data"]["status"], Order.Status.PAID)

    def test_cancel_restores_stock(self):
        self.login()
        profile = self.client.get("/api/v1/auth/profile/")
        from accounts.models import User

        user = User.objects.get(pk=profile.data["data"]["id"])
        address = Address.objects.create(user=user, recipient="李四", mobile="13900000000", province="上海市", city="上海市", district="浦东新区", detail="世纪大道")
        cart = self.client.post("/api/v1/cart/items/", {"product_id": self.product.id, "quantity": 3}, format="json")
        order = self.client.post("/api/v1/orders/orders/", {"address_id": address.id, "cart_item_ids": [cart.data["id"]]}, format="json")
        cancelled = self.client.post(f"/api/v1/orders/orders/{order.data['id']}/cancel/")
        self.assertEqual(cancelled.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)
