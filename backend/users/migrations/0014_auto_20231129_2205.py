# Generated by Django 3.2.3 on 2023-11-29 22:05

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20231129_0217'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='custombaseuser',
            name='name_not_me',
        ),
        migrations.AlterField(
            model_name='custombaseuser',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='custombaseuser',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='custombaseuser',
            name='username',
            field=models.CharField(max_length=100, unique=True, validators=[users.validators.validate_username]),
        ),
    ]