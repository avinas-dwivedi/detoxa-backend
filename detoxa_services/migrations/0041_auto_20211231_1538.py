# Generated by Django 3.2.5 on 2021-12-31 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0040_auto_20211230_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='childtracker',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='childtracker',
            name='last_name',
        ),
        migrations.AddField(
            model_name='childtracker',
            name='child',
            field=models.ForeignKey(db_column='child_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_child_id', to='detoxa_services.users'),
        ),
    ]
