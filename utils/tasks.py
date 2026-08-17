from celery import shared_task
from pathlib import Path
from dotenv import load_dotenv
from django.core.mail import EmailMultiAlternatives
from accounts.models import Email
from django.core.validators import validate_email
from django.utils import timezone
from django.template.loader import render_to_string
import string, random

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")

def random_string(string_length: int = 4):
    chars = string.digits
    return ''.join(random.sample(chars, string_length))

@shared_task(
        autoretry_for=(Exception,),
        retry_kwargs={"max_retries": 3},
        retry_backoff=True
)
def send_email(email: str, email_type: str, *args, **kwargs):
    if not validate_email(email):
        raise Exception("邮箱地址不对")
    last = Email.objects.filter(
        email=email,
        email_type=email_type,
    ).order_by("-create_at").first()
    if last and (timezone.now() - last.create_at).seconds < 60:
        return False, '发送邮件频繁，请稍后重试'
    code = random_string()
    if email_type == 'register':
        email_title = "小闲阁 - 注册账号"
        action_name = '注册账号'

    elif email_type == 'forget':
        email_title = "小闲阁 - 修改密码"
        action_name = "找回密码"
    elif email_type == 'change_email':
        email_title = "小闲阁 - 修改邮箱"
        action_name = '修改邮箱'
    elif email_type == "change_pwd":
        email_title = "小闲阁 - 修改密码"
        action_name = '修改密码'
    elif email_type == "complete":
        email_title = "小闲阁 - 补全信息"
        action_name = '补全信息'
    elif email_type == "delete":
        email_title = "小闲阁 -  注销账户"
        action_name = '注销账户'
    else:
        return False,"send_email发送错误，非法的发送类型"
    Email.objects.filter(
        email=email,
        email_type=email_type,
        is_active=True
    ).update(is_active=False)
    newRecord = Email.objects.create(
        email=email,
        email_type=email_type,
        code=code,
        is_active=True
    )
    subject = render_to_string('../templates/email.html', {
        "code": code,
        "action_name": action_name,
        "email_title": "小闲阁"
    })
    text_content = f"您的验证码是{code}, 五分钟内有效"
    try:
        res = EmailMultiAlternatives(
            subject=email_title,
            body=text_content,
            from_email="ghc245@163.com",
            to=[email],
        )
        res.attach_alternative(subject, 'text/html')
        res.send()
    except Exception as exc:
        print(f'邮件发送异常:{exc}')
    print(f"正在给{email}发送邮件，邮件类型：f{email_type}")
    return True, '发送成功'

