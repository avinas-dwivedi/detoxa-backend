# Generated by Django 3.2.5 on 2021-12-30 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0039_auto_20211229_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_organization_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='is_school_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='is_society_admin',
            field=models.BooleanField(default=False),
        ),
    ]