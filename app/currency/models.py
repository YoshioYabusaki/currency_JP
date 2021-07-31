from django.db import models


class Rate(models.Model):
    sale = models.DecimalField(max_digits=5, decimal_places=2)  # 123.45
    buy = models.DecimalField(max_digits=5, decimal_places=2)  # 123.45
    created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=32)  # examples: privatbank, monobank
    type = models.CharField(max_length=3)  # noqa


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
