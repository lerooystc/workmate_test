# Generated by Django 5.1.1 on 2024-09-30 16:00
import django.core.validators
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0002_cat_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cat",
            name="age",
            field=models.PositiveSmallIntegerField(
                validators=[django.core.validators.MaxValueValidator(240)],
                verbose_name="Возраст",
            ),
        ),
    ]
