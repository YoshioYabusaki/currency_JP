from currency import model_choices as mch
from currency import request_method_choices as rmch

from django.db import models


class Rate(models.Model):
    sale = models.DecimalField(max_digits=5, decimal_places=2)  # 123.45
    buy = models.DecimalField(max_digits=5, decimal_places=2)  # 123.45
    created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=32)  # examples: privatbank, monobank
    type = models.CharField(max_length=3, choices=mch.RATE_TYPES)  # noqa


class Source(models.Model):
    name = models.CharField(max_length=64)
    source_url = models.CharField(max_length=255)


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
