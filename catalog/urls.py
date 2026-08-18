from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import CategoryViewSet, ProductViewSet, GetProductViewSet, CourseViewSet, logout #GCourseList, GCourseDetail #course_list, course_detail

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("getProduct", GetProductViewSet, basename="getProduct")
router.register("courseLists", CourseViewSet, basename="courseList")
# router.register("courseDetails/<int:pk>/", CourseDetailViewSet, basename="courseDetail")
# router.register("course_list_all", course_list_all, basename="course_list_all")
paths = [
    path('logout/', logout),
    # path('course_detail/<int:pk>/', course_detail),
    # path('course_list_all/', course_list_all.as_view(), name='course_list_all'),
    # path("courseLists/", CourseViewSet.as_view({"get": "list", "post": "create"}), name="courseList"),
    # path("courseDetails/<int:pk>/", CourseViewSet.as_view({
    #     "get": "retrieve",
    #     "put": "update",
    #     "patch": "partial_update",
    #     "delete": "destroy"
    # }), name="courseDetail"),
]
urlpatterns = router.urls + paths
