# Generated by Django 3.2.5 on 2021-12-04 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0008_alter_doctor_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreport',
            name='report',
            field=models.CharField(default='', max_length=5000),
        ),
    ]
