# Generated by Django 3.2.5 on 2022-04-06 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0088_notifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='from_date',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='message',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='title',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='to_date',
        ),
    ]
