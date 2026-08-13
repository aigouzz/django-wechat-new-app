import hashlib

import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError


def exchange_code_for_openid(code: str) -> str:
    if settings.WECHAT_MOCK_LOGIN:
        return "mock_" + hashlib.sha256(code.encode()).hexdigest()[:48]
    if not settings.WECHAT_APP_ID or not settings.WECHAT_APP_SECRET:
        raise ValidationError("未配置微信AppID或AppSecret")
    response = requests.get(
        "https://api.weixin.qq.com/sns/jscode2session",
        params={
            "appid": settings.WECHAT_APP_ID,
            "secret": settings.WECHAT_APP_SECRET,
            "js_code": code,
            "grant_type": "authorization_code",
        },
        timeout=8,
    )
    response.raise_for_status()
    payload = response.json()
    if "openid" not in payload:
        raise AuthenticationFailed(payload.get("errmsg", "微信登录失败"))
    return payload["openid"]

