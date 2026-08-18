import json
import os

from dotenv import load_dotenv
from django.core.paginator import EmptyPage, InvalidPage, Page
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status, generics, mixins, pagination
from rest_framework.decorators import api_view, APIView

import jd.api
from common.exceptions import api_response

from .models import Category, Product, JDProduct, Course
from .serializers import CategorySerializer, ProductSerializer, JDProductSerializer, CourseSerializer
from .permissions import IsOwnerReadOnly
from utils.tasks import send_email

load_dotenv()


class CoursePagination(pagination.PageNumberPagination):
    """课程列表的页码分页。

    DRF 默认会把超出范围的页码作为 404 处理。列表页在数据刚好不足一页时
    仍可能请求下一页，因此这里返回保持分页结构的空结果，供客户端自然结束
    加载。
    """

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)
        try:
            self.page = paginator.page(page_number)
        except EmptyPage as exc:
            # Only numeric, out-of-range values reach EmptyPage. Invalid values
            # (for example `page=abc`) still receive DRF's normal validation.
            numeric_page_number = int(page_number)
            if numeric_page_number < 1:
                raise NotFound(
                    self.invalid_page_message.format(
                        page_number=page_number,
                        message=str(exc),
                    )
                )
            self.page = Page([], numeric_page_number, paginator)
        except InvalidPage as exc:
            raise NotFound(
                self.invalid_page_message.format(
                    page_number=page_number,
                    message=str(exc),
                )
            )

        if paginator.count > 1 and self.template is not None:
            self.display_page_controls = True

        return list(self.page)


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
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer
    pagination_class = CoursePagination
    permission_classes = [IsOwnerReadOnly]
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
