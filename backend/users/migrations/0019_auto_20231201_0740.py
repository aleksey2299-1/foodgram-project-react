# Generated by Django 3.2.3 on 2023-12-01 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_custombaseuser_subscribe'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='custombaseuser',
            options={'verbose_name': 'пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AddConstraint(
            model_name='custombaseuser',
            constraint=models.CheckConstraint(check=models.Q(('username__exact', 'me'), _negated=True), name='name_not_me'),
        ),
    ]