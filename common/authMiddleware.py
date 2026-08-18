import json, re, time
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from django.core.cache import cache

class AuthMiddleware(MiddlewareMixin):
    def __call__(self, request: HttpRequest):
        headers = request.headers
        authorization = headers.get("Authorization", "")
        if re.search("/wechat-login/|/swagger|/admin/", request.path):
            return self.get_response(request)
        else:
            if authorization:
                try:
                    access_token = AccessToken(authorization)
                    user_id = access_token['user_id']
                    expire_time = access_token.payload.get('exp')
                    user_obj = User.objects.get(id=user_id)
                    key = f'user_manage:logout:{user_obj.nickname}:expire_token'
                    auth_list = cache.get(key)
                    access_token = json.loads(auth_list) if auth_list else {}
                    if access_token and access_token.expire_time and access_token.expire_time < int(time.time()):
                        cache.delete(key)
                    if authorization == access_token.token:
                        return JsonResponse({
                            "code": 400,
                            "message": "token失效",
                            "data": {}
                        })
                except Exception as exc:
                    return JsonResponse({
                                "code": 406,
                                "message": exc.__str__(),
                                "data": {}
                            })
            else:
                return JsonResponse({
                            "code": 401,
                            "message": "没有登录",
                            "data": {}
                        })
        return self.get_response(request)