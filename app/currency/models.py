from django.db import models

class Rate(models.Model):
    sale = models.DecimalField(max_digits=5, decimal_places=2)  # 123.45
    buy = models.DecimalField(max_digits=5, decimal_places=2)  # 123.45
    created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=32)  # examples: privatbank, monobank
    type = models.CharField(max_length=32)  # examples: USD, EUR


# class ContactUs # -> currency_contactus