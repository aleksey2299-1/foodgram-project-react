# Generated by Django 3.2.3 on 2023-11-24 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_custombaseuser_subscribe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='custombaseuser',
            name='subscribe',
        ),
    ]
