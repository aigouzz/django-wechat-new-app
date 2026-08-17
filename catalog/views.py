import json
import os

from dotenv import load_dotenv
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
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

lists1 = {
    'name': 'jd',
    'price': 11.7,
    'created_at': '2026-12-22 12:33:22'
}

# @api_view(['GET', 'POST'])
# def course_list(request):
#     if request.method == 'GET':
#         s = CourseSerializer(instance=Course.objects.all(), many=True)
#         return Response(data=s.data, status=status.HTTP_200_OK)
#     else:
#         s = CourseSerializer(data=request.data) # 部分更新 partial=True
#         if s.is_valid():
#             s.save(teacher=request.user)
#             return Response(data=s.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def course_detail(request, pk):
#     try:
#         course = Course.objects.get(pk=pk)
#     except Course.DoesNotExist:
#         return Response(data={"msg": "没有这个课程信息"}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         s = CourseSerializer(instance=course)
#         return Response(data=s.data, status=status.HTTP_200_OK)
#     elif request.method == 'PUT':
#         s = CourseSerializer(instance=course, data=request.data)
#         if s.is_valid():
#             s.save()
#             return Response(data=s.data, status=status.HTTP_200_OK)
#         return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         course.delete()
#         return Response(data={'msg': "ok"}, status=status.HTTP_200_OK)
#     else:
#         return Response(data={"msg": "不允许这种请求"}, status=status.HTTP_400_BAD_REQUEST) 

class CourseList(APIView):
    def get(self, request):
        queryset = Course.objects.all()
        s = CourseSerializer(instance=queryset, many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)
    def post(self, request):
        s = CourseSerializer(data=request.data)
        if s.is_valid():
            s.save(teacher=self.request.user)
            print(type(request.data), type(s.data))
            return Response(data=s.data, status=status.HTTP_200_OK)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)