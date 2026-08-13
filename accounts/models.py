from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    openid = models.CharField("微信OpenID", max_length=64, unique=True, null=True, blank=True)
    nickname = models.CharField("昵称", max_length=50, blank=True)
    avatar_url = models.URLField("头像", max_length=500, blank=True)
    mobile = models.CharField("手机号", max_length=20, blank=True)
    is_disabled = models.SmallIntegerField("是否禁用", default=0)

    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "accounts_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

