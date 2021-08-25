from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        default=None,
    )

    email = models.EmailField('email address', blank=True, unique=True)
