# Generated by Django 3.2.3 on 2023-11-24 01:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_custombaseuser_subscribe'),
    ]

    operations = [
        migrations.AddField(
            model_name='custombaseuser',
            name='subscribe',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
