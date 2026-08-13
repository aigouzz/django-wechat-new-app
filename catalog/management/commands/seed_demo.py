from decimal import Decimal

from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "创建演示商品"

    def handle(self, *args, **options):
        categories = {}
        for index, name in enumerate(("精选", "数码", "生活")):
            categories[name], _ = Category.objects.get_or_create(name=name, defaults={"sort_order": index})
        products = (
            ("精选", "无线蓝牙耳机", "299.00", 100),
            ("数码", "机械键盘", "399.00", 80),
            ("生活", "保温随行杯", "89.00", 200),
        )
        for category_name, name, price, stock in products:
            Product.objects.get_or_create(
                name=name,
                defaults={"category": categories[category_name], "price": Decimal(price), "stock": stock, "description": f"高品质{name}"},
            )
        self.stdout.write(self.style.SUCCESS("演示数据创建完成"))

