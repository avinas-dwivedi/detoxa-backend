# Generated by Django 3.2.5 on 2021-12-02 14:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0004_auto_20211202_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'specialization',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Doctors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('degree_name', models.CharField(max_length=50, null=True)),
                ('experience', models.CharField(max_length=100, null=True)),
                ('profile_image_key', models.CharField(max_length=255, null=True)),
                ('profile_image_extension', models.CharField(max_length=20, null=True)),
                ('email', models.EmailField(max_length=200, null=True, unique=True, validators=[django.core.validators.EmailValidator])),
                ('mobile', models.CharField(max_length=30, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: 919999999999 of length 11 to 14.', regex='^\\d{11,13}$')])),
                ('time_slots', models.CharField(max_length=4000, null=True)),
                ('consultation_fee', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('specialization', models.ForeignKey(db_column='specialization_id', on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.specialization')),
            ],
            options={
                'db_table': 'doctors',
                'managed': True,
            },
        ),
    ]
