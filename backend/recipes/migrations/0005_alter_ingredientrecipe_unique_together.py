# Generated by Django 3.2.3 on 2023-11-25 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_ingredientrecipe_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ingredientrecipe',
            unique_together=set(),
        ),
    ]
