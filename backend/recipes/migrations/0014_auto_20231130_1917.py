# Generated by Django 3.2.3 on 2023-11-30 19:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0013_auto_20231130_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='added_to_favorites',
            field=models.ManyToManyField(related_name='added_to_favorites', to=settings.AUTH_USER_MODEL, verbose_name='Объекты избранного'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='shopping_cart',
            field=models.ManyToManyField(related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='Объекты корзины'),
        ),
    ]
