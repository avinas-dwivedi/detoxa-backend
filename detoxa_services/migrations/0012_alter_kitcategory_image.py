# Generated by Django 3.2.5 on 2021-12-09 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0011_kitcategory_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitcategory',
            name='image',
            field=models.URLField(blank=True, max_length=2000),
        ),
    ]