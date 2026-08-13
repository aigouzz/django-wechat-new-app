from django.urls import path

from .views import profile, refresh_token, wechat_login

urlpatterns = [
    path("wechat-login/", wechat_login),
    path("token/refresh/", refresh_token),
    path("profile/", profile),
]

