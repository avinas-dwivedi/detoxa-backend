# Generated by Django 3.2.5 on 2021-12-31 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0045_handeyetracker_child'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='handeyetracker',
            name='age',
        ),
        migrations.RemoveField(
            model_name='handeyetracker',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='handeyetracker',
            name='last_name',
        ),
    ]