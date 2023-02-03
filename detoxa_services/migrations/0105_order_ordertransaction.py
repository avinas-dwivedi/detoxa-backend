# Generated by Django 3.2.5 on 2022-05-13 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0104_auto_20220508_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_items', models.JSONField()),
                ('order_status', models.CharField(max_length=255)),
                ('order_total', models.FloatField()),
                ('order_updated_at', models.DateTimeField(auto_now=True)),
                ('order_created_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.users')),
            ],
        ),
        migrations.CreateModel(
            name='OrderTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_gateway', models.CharField(default='Razorpay', max_length=20)),
                ('payment_id', models.CharField(max_length=100, null=True)),
                ('signature', models.CharField(max_length=100, null=True)),
                ('transaction_datetime', models.DateTimeField(auto_now_add=True)),
                ('orde', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='detoxa_services.order')),
            ],
        ),
    ]