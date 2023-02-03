# Generated by Django 3.2.5 on 2022-05-13 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0105_order_ordertransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Success', 'Success'), ('Cancelled', 'Cancelled')], max_length=255),
        ),
    ]
