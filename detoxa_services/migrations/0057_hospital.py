# Generated by Django 3.2.5 on 2022-01-12 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0056_auto_20220108_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('total_no_of_doctors', models.IntegerField(default=0)),
                ('logo', models.URLField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='detoxa_services.users')),
            ],
            options={
                'db_table': 'hospital',
                'managed': True,
            },
        ),
    ]
