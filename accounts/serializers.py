from rest_framework import serializers

from .models import User


class WeChatLoginSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=128)
    nickname = serializers.CharField(max_length=50, required=False, allow_blank=True)
    avatar_url = serializers.URLField(required=False, allow_blank=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "nickname", "avatar_url", "mobile", "date_joined")
        read_only_fields = ("id", "username", "date_joined")

