# Generated by Django 3.2.3 on 2023-11-24 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_custombaseuser_subscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custombaseuser',
            name='username',
            field=models.SlugField(max_length=40, unique=True),
        ),
    ]
