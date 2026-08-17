from django.db import models
from uuid_extensions import uuid7 as uuid7_factory


def generate_uuid7():
    """生成可被 Django 迁移安全引用的 UUIDv7。"""
    return uuid7_factory()


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


class JDProduct(models.Model):
    # jd_uuid = models.UUIDField(
    #     primary_key=True,
    #     default=generate_uuid7,
    #     editable=False,
    #     verbose_name="商品UUID",
    # )
    categoryInfo = models.JSONField(default=dict, blank=True, verbose_name="类目信息")
    comments = models.IntegerField(verbose_name="评论数")
    commissionInfo = models.JSONField(default=dict, blank=True, verbose_name="佣金信息")
    couponInfo = models.JSONField(default=dict, blank=True, verbose_name="优惠券信息")
    goodCommentsShare = models.FloatField(verbose_name="商品好评率")
    imageInfo = models.JSONField(default=dict, blank=True, verbose_name="图片信息")
    inOrderCount30Days = models.IntegerField(verbose_name="30天引单数量")
    materialUrl = models.CharField(max_length=256, verbose_name="联盟商品链接")
    priceInfo = models.JSONField(default=dict, blank=True, verbose_name="价格信息")
    shopInfo = models.JSONField(default=dict, blank=True, verbose_name="店铺信息")
    skuId = models.BigIntegerField(unique=True, verbose_name="商品id")
    skuName = models.CharField(max_length=256, verbose_name="商品名称")
    isHot = models.BooleanField(default=False, verbose_name="是否爆款")
    spuid = models.BigIntegerField(null=True, blank=True, verbose_name="同款商品主SKU ID")
    brandCode = models.CharField(max_length=64, blank=True, verbose_name="品牌编码")
    brandName = models.CharField(max_length=128, blank=True, verbose_name="品牌名称")
    owner = models.CharField(max_length=1, blank=True, verbose_name="商品类型")
    pinGouInfo = models.JSONField(default=dict, blank=True, verbose_name="拼购信息")
    resourceInfo = models.JSONField(default=dict, blank=True, verbose_name="资源信息")
    inOrderCount30DaysSku = models.IntegerField(default=0, verbose_name="30天SKU引单数量")
    seckillInfo = models.JSONField(default=dict, blank=True, verbose_name="秒杀信息")
    jxFlags = models.JSONField(default=list, blank=True, verbose_name="京喜商品类型")
    videoInfo = models.JSONField(default=dict, blank=True, verbose_name="视频信息")
    documentInfo = models.JSONField(default=dict, blank=True, verbose_name="文案信息")
    bookInfo = models.JSONField(default=dict, blank=True, verbose_name="图书信息")
    forbidTypes = models.JSONField(default=list, blank=True, verbose_name="禁售类型")
    deliveryType = models.BooleanField(default=False, verbose_name="是否京东配送")
    skuLabelInfo = models.JSONField(default=dict, blank=True, verbose_name="商品标签")
    promotionLabelInfoList = models.JSONField(
        default=list, blank=True, verbose_name="商品促销标签集"
    )
    secondPriceInfoList = models.JSONField(default=list, blank=True, verbose_name="双价格信息")
    preSaleInfo = models.JSONField(default=dict, blank=True, verbose_name="预售信息")
    reserveInfo = models.JSONField(default=dict, blank=True, verbose_name="预约信息")
    solitaireActivity = models.JSONField(default=dict, blank=True, verbose_name="订单接龙活动信息")
    isOversea = models.BooleanField(default=False, verbose_name="是否全球购商品")
    companyType = models.IntegerField(null=True, blank=True, verbose_name="商家类型")
    purchasePriceInfo = models.JSONField(default=dict, blank=True, verbose_name="到手价明细")
    bonusInfoList = models.JSONField(default=list, blank=True, verbose_name="联盟奖励活动集合")
    activityCardInfo = models.JSONField(default=dict, blank=True, verbose_name="超市购物卡明细")
    smartDocumentInfoList = models.JSONField(
        default=list, blank=True, verbose_name="智能推广文案集合"
    )
    kaAdowner = models.BooleanField(default=False, verbose_name="是否星选商家商品")
    itemId = models.CharField(max_length=128, blank=True, db_index=True, verbose_name="联盟商品ID")
    skuTagList = models.JSONField(default=list, blank=True, verbose_name="联盟标签")
    specialSkuUrlInfo = models.JSONField(default=dict, blank=True, verbose_name="频道页信息")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "catalog_jd_product"
        ordering = ("-created_at",)
        verbose_name = "京东商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.skuName

class Channel(models.Model): # 分类
    channel_id = models.IntegerField( null=False, verbose_name='类目id')
    name = models.CharField(max_length=48, verbose_name='类目名称')
    grade = models.SmallIntegerField( verbose_name='类目级别(类目级别 0，1，2 代表一、二、三级类目)')
    parentId = models.IntegerField( verbose_name='主类目id')