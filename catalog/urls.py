from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import CategoryViewSet, ProductViewSet, GetProductViewSet, CourseList #course_list, course_detail

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("getProduct", GetProductViewSet, basename="getProduct")
# router.register("courseList", CourseList, basename="courseList")
# router.register("course_list", course_list, basename="course_list")
# router.register("course_list_all", course_list_all, basename="course_list_all")
paths = [
    # path('course_list/', course_list),
    # path('course_detail/<int:pk>/', course_detail),
    # path('course_list_all/', course_list_all.as_view(), name='course_list_all'),
    path("courseList/", CourseList.as_view(), name="courseList")
]
urlpatterns = router.urls + paths
