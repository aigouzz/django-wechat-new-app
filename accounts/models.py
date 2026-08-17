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

class Email(models.Model):
    SEND_TYPE_CHOICES = (
        ("register","注册"),
        ("forget","找回密码"),
        ("change_pwd",'修改密码'),
        ('change_email_new','修改邮箱'),
        ('complete',"补全信息"),
        ('delete',"注销账号")
    )
    code = models.CharField(max_length=20, verbose_name="发送的验证码")
    email = models.CharField(max_length=64, null=False, verbose_name="邮件地址")
    email_type = models.CharField(max_length=20, choices=SEND_TYPE_CHOICES, default='register', null=False, verbose_name='邮件类型')
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

