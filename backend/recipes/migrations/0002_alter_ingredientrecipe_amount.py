# Generated by Django 3.2.3 on 2023-11-25 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]