import uuid

from accounts.models import User

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def update_user_phone(sender, instance, **kwargs):
    # print('SIGNAL PRE SAVE USER')
    if instance.phone:
        instance.phone = ''.join(char for char in instance.phone if char.isdigit())


@receiver(pre_save, sender=User)
def set_user_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = str(uuid.uuid4())


@receiver(post_save, sender=User)
def user_post_save(sender, instance, **kwargs):
    print('SIGNAL POST SAVE USER')  # noqa
