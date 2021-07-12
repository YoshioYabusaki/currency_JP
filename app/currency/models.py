from django.db import models


class Rate(models.Model):
    sale = models.DecimalField(max_digits=5, decimal_places=2)  # 123.45
    buy = models.DecimalField(max_digits=5, decimal_places=2)  # 123.45
    created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=32)  # examples: privatbank, monobank
    type = models.CharField(max_length=3)  # noqa


class ContactUs(models.Model):
    user_name = models.CharField(max_length=35)
    email_form = models.EmailField(max_length=254)
    subject = models.CharField(max_length=50)
    message = models.TextField()
