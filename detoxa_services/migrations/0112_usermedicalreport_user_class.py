# Generated by Django 3.2.5 on 2022-05-15 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0111_bankdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermedicalreport',
            name='user_class',
            field=models.CharField(default='', max_length=100),
        ),
    ]