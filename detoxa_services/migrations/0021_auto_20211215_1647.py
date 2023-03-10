# Generated by Django 3.2.5 on 2021-12-15 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0020_auto_20211214_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='is_cancelled',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='is_completed',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='is_upcoming',
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Rescheduled', 'Rescheduled'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
