from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import profile, refresh_token, wechat_login

urlpatterns = [
    path("wechat-login/", wechat_login),
    path("token/refresh/", refresh_token),
    path("profile/", profile),
    path("api/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/refresh", TokenRefreshView.as_view(), name="token_refresh_pair"),
]

