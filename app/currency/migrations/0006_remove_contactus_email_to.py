# Generated by Django 3.2.5 on 2021-07-30 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0005_auto_20210730_0639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactus',
            name='email_to',
        ),
    ]