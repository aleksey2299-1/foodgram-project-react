# Generated by Django 3.2.3 on 2023-11-25 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20231125_1841'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ingredientrecipe',
            unique_together={('recipe', 'ingredient')},
        ),
    ]