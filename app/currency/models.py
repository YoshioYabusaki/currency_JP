from currency import model_choices as mch
from currency import request_method_choices as rmch

from django.db import models


def upload_logo(instance, filename):
    return f'logos/{instance.id}/{filename}'


class Source(models.Model):
    name = models.CharField(max_length=64)
    source_url = models.CharField(max_length=255)
    logo = models.FileField(
        upload_to=upload_logo,
        blank=True,
        null=True,
        default=None,
    )
    code_name = models.CharField(max_length=24, unique=True, editable=False)


class Rate(models.Model):
    sale = models.DecimalField(max_digits=5, decimal_places=2)  # 123.45
    buy = models.DecimalField(max_digits=5, decimal_places=2)  # 123.45
    created = models.DateTimeField(auto_now_add=True)
    # source = models.CharField(max_length=32)
    source = models.ForeignKey(
        Source,
        related_name='rates',
        on_delete=models.CASCADE,  # もしSourceでデータ消去の場合、関連のRateも消去。.SET_NULLも便利。
    )
    type = models.CharField(  # noqa
        max_length=3,
        choices=mch.RATE_TYPES,
        blank=False,
        null=False,
        default=mch.TYPE_USD,
    )


class ContactUs(models.Model):
    user_name = models.CharField(max_length=35)
    email_form = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=2050)
    created = models.DateTimeField(auto_now_add=True)


class GoodCafe(models.Model):
    cafe_name = models.CharField(max_length=35)
    open_time = models.CharField(max_length=9)
    close_time = models.CharField(max_length=9)
    address = models.CharField(max_length=50)
    recommended_menu = models.CharField(max_length=50)


class ResponseLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status_code = models.PositiveSmallIntegerField()
    path = models.CharField(max_length=255)
    response_time = models.PositiveSmallIntegerField(help_text='in milliseconds')
    request_method = models.CharField(max_length=4, choices=rmch.REQUEST_METHOD)
