# Generated by Django 3.2.5 on 2022-01-12 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0057_hospital'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_hospital_admin',
            field=models.BooleanField(default=False),
        ),
    ]