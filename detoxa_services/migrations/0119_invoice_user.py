# Generated by Django 3.2.5 on 2022-05-22 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0118_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='detoxa_services.users'),
        ),
    ]
