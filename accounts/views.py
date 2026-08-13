from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from common.exceptions import api_response

from .models import User
from .serializers import UserSerializer, WeChatLoginSerializer
from .services import exchange_code_for_openid


@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def wechat_login(request):
    serializer = WeChatLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    openid = exchange_code_for_openid(serializer.validated_data["code"])
    user, _ = User.objects.get_or_create(
        openid=openid,
        defaults={
            "username": f"wx_{openid[-24:]}",
            "nickname": serializer.validated_data.get("nickname", "微信用户"),
            "avatar_url": serializer.validated_data.get("avatar_url", ""),
        },
    )
    refresh = RefreshToken.for_user(user)
    return api_response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(request):
    serializer = TokenRefreshSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return api_response(serializer.validated_data)


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == "PATCH":
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    return api_response(UserSerializer(request.user).data)

