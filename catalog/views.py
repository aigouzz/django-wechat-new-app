import json
import os

from dotenv import load_dotenv
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, APIView

import jd.api
from common.exceptions import api_response

from .models import Category, Product, JDProduct, Course
from .serializers import CategorySerializer, ProductSerializer, JDProductSerializer, CourseSerializer
from utils.tasks import send_email

load_dotenv()

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

class GetProductViewSet(ViewSet):
    """从京东联盟拉取商品；不对应本地数据库模型。"""
    permission_classes = (AllowAny,)

    def list(self, request):
        jd.setDefaultAppInfo(os.environ['APP_KEY'], os.environ['SECRET_KEY'])
        a = jd.api.UnionOpenGoodsJingfenQueryRequest()
        a.goodsReq = {
            'eliteId': 22,
            'pageIndex': 1,
            'sortName': 'goodComments'
        }
        f = a.getResponse(os.environ['RIGHT_KEY'])
        print(f.get('jd_union_open_goods_jingfen_query_responce'))
        datas = f.get('jd_union_open_goods_jingfen_query_responce').get('queryResult')
        if type(datas) is str:
            result = json.loads(datas).get('data', [])
        elif type(datas) is dict:
            result = datas.get('data', [])
        else:
            result = []
        for item in result:
            nowItem = JDProduct.objects.filter(
                skuId=item.skuId
            )
            if nowItem:
                continue
            else:
                # JDProduct.objects.create()
                pass
        data = {}
        return api_response(data=data)

class RegisterViewSet(ViewSet):
    """发送邮件"""
    permission_classes = (AllowAny,)

    def list(self, request):
        pass

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

